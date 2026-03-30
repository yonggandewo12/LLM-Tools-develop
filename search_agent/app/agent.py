import os

from langchain.agents import create_agent
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from app.llm import get_llm
from app.search import search_tool

_llm = None
_db_path = os.path.join(os.path.dirname(__file__), "..", "chat_memory.db")


def _get_llm():
    global _llm
    if _llm is None:
        _llm = get_llm()
    return _llm


async def stream_answer(query: str, session_id: str = "default"):
    config = {"configurable": {"thread_id": session_id}}
    llm = _get_llm()

    async with AsyncSqliteSaver.from_conn_string(_db_path) as checkpointer:
        await checkpointer.setup()
        agent = create_agent(
            model=llm,
            tools=[search_tool],
            system_prompt="你是智能助手，可使用搜索工具。回答简洁、有条理，记住用户之前说过的内容。",
            checkpointer=checkpointer,
        )

        async for event in agent.astream_events(
            {"messages": [("user", query)]},
            version="v1",
            config=config,
        ):
            if event["event"] == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield f"data: {content}\n\n"
