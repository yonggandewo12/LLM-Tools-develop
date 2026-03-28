from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from app.agent import stream_answer
from app.config import SEARCH_ENGINE, LLM_MODEL

app = FastAPI(
    title="本地LLM+搜索智能服务",
    description="搜索不可用自动纯本地运行",
    version="1.0"
)

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <div style="text-align:center; margin-top:100px; font-size:18px;">
        <h1>✅ 服务运行中</h1>
        <p><a href="/docs" target="_blank">打开接口调试UI</a></p>
    </div>
    """

@app.post("/api/chat")
async def chat(query: str):
    return StreamingResponse(
        stream_answer(query),
        media_type="text/event-stream"
    )

@app.get("/status")
def status():
    return {
        "status": "running",
        "search_engine": SEARCH_ENGINE,
        "model": LLM_MODEL
    }