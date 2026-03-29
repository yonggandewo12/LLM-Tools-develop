from app.config import (
    SEARCH_ENGINE,
    TAVILY_API_KEY,
    TAVILY_MAX_RESULTS,
    SEARXNG_API_URL,
    SEARXNG_MAX_RESULTS
)
import requests

def tavily_search(query: str) -> str | None:
    try:
        if not TAVILY_API_KEY:
            return None
        resp = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": TAVILY_MAX_RESULTS,
                "lang": "zh"
            }, timeout=8
        )
        if resp.status_code == 200:
            return str(resp.json())
        return None
    except Exception:
        return None

def searxng_search(query: str) -> str | None:
    try:
        resp = requests.get(
            f"{SEARXNG_API_URL}/search",
            params={
                "q": query,
                "format": "json",
                "engines": "baidu,bing,duckduckgo",
                "num": SEARXNG_MAX_RESULTS,
                "language": "zh"
            }, timeout=8
        )
        if resp.status_code == 200:
            return str(resp.json())
        return None
    except Exception:
        return None

def web_search(query: str) -> str | None:
    if SEARCH_ENGINE == "searxng":
        res = searxng_search(query)
        if res is not None:
            return res
        return tavily_search(query)
    else:
        return tavily_search(query)

from langchain.tools import tool

@tool
def search_tool(query: str) -> str:
    """联网搜索工具，根据用户问题搜索相关信息。"""
    return web_search(query) or "搜索不可用"