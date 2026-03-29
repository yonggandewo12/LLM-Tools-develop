from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from pydantic import BaseModel
from app.agent import stream_answer
from app.config import SEARCH_ENGINE, LLM_MODEL
import os

# OpenAPI标准请求体模型
class ChatRequest(BaseModel):
    query: str
    session_id: str = "default"

app = FastAPI(
    title="本地LLM+搜索智能服务",
    description="搜索不可用自动纯本地运行",
    version="1.0"
)

# 配置CORS允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <div style="text-align:center; margin-top:100px; font-size:18px;">
        <h1>✅ 服务运行中</h1>
        <p><a href="/v1/chat" target="_blank">打开聊天界面</a></p>
        <p><a href="/docs" target="_blank">打开接口调试UI</a></p>
    </div>
    """

@app.get("/v1/chat", response_class=HTMLResponse)
async def chat_page():
    chat_file_path = os.path.join(os.path.dirname(__file__), "chat.html")
    return FileResponse(chat_file_path)

@app.post("/v1/chat/completions")
async def chat(request: ChatRequest):
    """标准OpenAPI聊天接口"""
    return StreamingResponse(
        stream_answer(request.query, session_id=request.session_id),
        media_type="text/event-stream"
    )

@app.get("/status")
def status():
    return {
        "status": "running",
        "search_engine": SEARCH_ENGINE,
        "model": LLM_MODEL
    }