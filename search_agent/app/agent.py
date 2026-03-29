from langchain.agents import create_agent
from app.llm import get_llm
from app.search import search_tool, web_search

_llm = None
_agent = None

def _get_agent():
    global _llm, _agent
    if _llm is None:
        _llm = get_llm()
    if _agent is None:
        _agent = create_agent(
            model=_llm,
            tools=[search_tool],
            system_prompt="你是智能助手，可使用搜索工具。回答简洁、有条理。"
        )
    return _agent

async def stream_answer(query: str):
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
        version="v1"
    ):
        if event["event"] == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                yield f"data: {content}\n\n"