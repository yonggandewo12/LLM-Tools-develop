from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from app.llm import get_llm
from app.search import search_tool, web_search

llm = get_llm()
tools = [search_tool]

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是智能助手，可使用搜索工具。回答简洁、有条理。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

async def stream_answer(query: str):
    search_result = web_search(query)
    if search_result is None:
        async for chunk in llm.astream(query):
            content = chunk.content
            if content:
                yield f"data: {content}\n\n"
        return

    async for event in agent_executor.astream_events(
        {"input": query},
        version="v1"
    ):
        if event["event"] == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                yield f"data: {content}\n\n"