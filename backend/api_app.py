import os
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import asyncio
import uvicorn
from schemas import ChatRequest, ChatResponse
from chat_func import chat_with_llama
import uuid
import chromadb
from chromadb import PersistentClient
from fastapi_mcp import FastApiMCP
# loggerのインポート
import logging
import sys
from logging import StreamHandler, Formatter

# loggerの設定
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)
handler = StreamHandler(sys.stdout)
handler.setFormatter(Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

api_app = FastAPI(title="チャットAPI")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# キャッシュの初期化
@api_app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# 基本的なエンドポイント（キャッシュ付き）
@api_app.get("/")
@cache(expire=60)
async def hello():
    return {"message": "Hello World!"}

# チャットエンドポイント
@api_app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 会話履歴を更新
    history = request.history or []
    history.append({"role": "user", "content": request.user_message})

    # モデル名をリクエストから取得し、パスを設定
    model_name = request.model_name or "Llama-3-ELYZA-JP-8B-q4_k_m.gguf"
    model_path = os.path.join("./local_llms", model_name)

    # モデルファイルが存在するか確認
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail=f"Model file not found: {model_path}")

    # Llamaモデルを使用して応答を生成
    bot_message = chat_with_llama(model_path, request.user_message)

    # 応答を履歴に追加
    history.append({"role": "bot", "content": bot_message})

    return ChatResponse(bot_message=bot_message, history=history)

# テキストファイルをアップロードしてChromaDBに格納するエンドポイント
@api_app.post("/upload_files")
async def upload_file(file: UploadFile = File(...)):
    # ファイルの内容を読み取る
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")

    content = await file.read()
    text_data = content.decode("utf-8")

    # UUIDを生成してDBの格納先を決定
    db_id = str(uuid.uuid4())
    # DBの格納先ディレクトリを指定
    persist_directory = f"./chromadb/{db_id}"

    # デバッグ用ログを追加
    logger.debug(f"Persist directory: {persist_directory}")

    # ChromaDBクライアントを初期化
    client = chromadb.PersistentClient(path=persist_directory)
    # コレクションを作成し、テキストデータを格納
    collection = client.create_collection(name="text_collection")
    collection.add(documents=[text_data], metadatas=[{"filename": file.filename}], ids=[db_id])
    logger.debug(collection.peek())
    return {"message": "File uploaded and processed successfully", "db_id": db_id}

@api_app.get("/hello", tags=["MCP"], operation_id="say_hello")
async def hello():
    """シンプルな挨拶エンドポイント"""
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("api_app:api_app", host="0.0.0.0", port=8000, reload=True)