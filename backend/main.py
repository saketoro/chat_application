import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import asyncio
import uvicorn
from schemas import ChatRequest, ChatResponse
from chat_func import chat_with_llama

app = FastAPI(title="チャットAPI")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# キャッシュの初期化
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# 基本的なエンドポイント（キャッシュ付き）
@app.get("/")
@cache(expire=60)
async def hello():
    return {"message": "Hello World!"}

# チャットエンドポイント
@app.post("/chat", response_model=ChatResponse)
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)