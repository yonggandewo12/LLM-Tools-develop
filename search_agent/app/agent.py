from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import trim_messages
from app.llm import get_llm
from app.search import search_tool, web_search
from app.config import MEMORY_MAX_MESSAGES

_llm = None
_agent = None
# 内存级记忆（重启后丢失），如需持久化请用PostgreSQL
_checkpointer = InMemorySaver()

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