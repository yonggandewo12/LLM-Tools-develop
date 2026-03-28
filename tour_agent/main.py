from fastapi import FastAPI
from core.search import web_search
from core.weather import get_weather
from core.tour import recommend_attractions

app = FastAPI(title="本地大模型旅游助手API", version="1.0")

@app.get("/")
def home():
    return {"msg": "旅游助手API运行中", "docs": "/docs"}

# 1 联网搜索
@app.get("/api/search")
def api_search(q: str):
    return {"query": q, "results": web_search(q)}

# 2 天气查询
@app.get("/api/weather")
def api_weather(city: str):
    return {"city": city, "weather": get_weather(city)}

# 3 景点推荐
@app.get("/api/tour/recommend")
def api_tour(city: str):
    return {"city": city, "recommend": recommend_attractions(city)}

# 智能问答（本地LLM + 联网）
@app.get("/api/chat")
def api_chat(q: str):
    from core.llm import get_local_llm
    llm = get_local_llm()
    search_res = web_search(q)
    if isinstance(search_res, dict) and "error" in search_res:
        return {"query": q, "answer": "抱歉，搜索服务暂时不可用，无法提供实时信息。"}
    info = "\n".join([r["snippet"] for r in search_res[:3]])
    prompt = f"用户问题：{q}\n参考信息：{info}\n请用中文简洁回答："
    ans = llm.invoke(prompt).content
    return {"query": q, "answer": ans}
