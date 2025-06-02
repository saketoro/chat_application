import uvicorn
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from api_app import api_app

# 公開するAPIのエンドポイントを指定

# MCPサーバーを作成
mcp_app = FastAPI()
mcp = FastApiMCP(api_app, name="MCP Server", include_tags=["MCP"])
mcp.mount(mcp_app)

if __name__ == "__main__":
    uvicorn.run("mcp_app:mcp_app", host="0.0.0.0", port=8001, reload=True)