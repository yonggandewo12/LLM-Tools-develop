from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import trim_messages
from app.llm import get_llm
from app.search import search_tool, web_search
from app.config import MEMORY_MAX_MESSAGES
import sqlite3
import os

_llm = None
_agent = None

# SQLite持久化存储，重启后记忆不丢失
_db_path = os.path.join(os.path.dirname(__file__), "..", "chat_memory.db")
_conn = sqlite3.connect(_db_path, check_same_thread=False)
_checkpointer = SqliteSaver(_conn)
# 初始化数据库表
_checkpointer.setup()

def _get_agent():
    global _llm, _agent
    if _llm is None:
        _llm = get_llm()
    if _agent is None:
        _agent = create_agent(
            model=_llm,
            tools=[search_tool],
            system_prompt="你是智能助手，可使用搜索工具。回答简洁、有条理，记住用户之前说过的内容。",
            checkpointer=_checkpointer
        )
    return _agent

async def stream_answer(query: str, session_id: str = "default"):
    """
    流式回答用户问题，支持会话记忆
    :param query: 用户问题
    :param session_id: 会话ID，不同ID对应独立记忆
    """
    config = {"configurable": {"thread_id": session_id}}
    
    # 搜索降级逻辑：搜索失败直接用纯LLM回答
    search_result = web_search(query)
    if search_result is None:
        llm = get_llm()
        async for chunk in llm.astream(query):
            content = chunk.content
            if content:
                yield f"data: {content}\n\n"
        return

    agent = _get_agent()
    async for event in agent.astream_events(
        {"messages": [("user", query)]},
        version="v1",
        config=config
    ):
        if event["event"] == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                yield f"data: {content}\n\n"