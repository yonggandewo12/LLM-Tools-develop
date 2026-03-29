from app.config import (
    DDG_MAX_RESULTS,
    DDG_REGION,
    DDG_TIMEOUT
)
import requests
import json

def duckduckgo_search(query: str) -> str | None:
    """DuckDuckGo 搜索后端（无额外依赖，直接调用公开API）"""
    try:
        # 优先使用HTML搜索，结果更丰富
        resp = requests.get(
            "https://html.duckduckgo.com/html/",
            params={
                "q": query,
                "kl": DDG_REGION,
                "df": "m",
                "k1": -1  # 关闭安全搜索
            },
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            timeout=DDG_TIMEOUT
        )
        if resp.status_code != 200:
            return None
            
        # 简单解析HTML结果
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = soup.select('.result')
        
        if not results:
            # 降级到API搜索
            resp = requests.get(
                "https://api.duckduckgo.com/",
                params={
                    "q": query,
                    "format": "json",
                    "no_html": 1,
                    "skip_disambig": 1,
                    "kl": DDG_REGION
                },
                timeout=DDG_TIMEOUT
            )
            if resp.status_code == 200:
                data = resp.json()
                abstract = data.get("Abstract", "")
                if abstract:
                    return f"[摘要] {data.get('Heading', '')}\n{abstract}\n链接: {data.get('AbstractURL', '')}"
            return None
            
        # 格式化为易读的文本
        formatted = []
        for idx, r in enumerate(results[:DDG_MAX_RESULTS], 1):
            title_elem = r.select_one('.result__a')
            body_elem = r.select_one('.result__snippet')
            href_elem = r.select_one('.result__a')
            
            if title_elem and body_elem and href_elem:
                title = title_elem.get_text(strip=True)
                body = body_elem.get_text(strip=True)
                href = href_elem.get('href', '')
                if title and body:
                    formatted.append(f"[{idx}] {title}\n{body}\n链接: {href}\n")
        
        return "\n---\n".join(formatted) if formatted else None
        
    except Exception:
        return None

def web_search(query: str) -> str | None:
    """搜索主入口，使用DuckDuckGo作为唯一搜索后端"""
    return duckduckgo_search(query)

from langchain.tools import tool

@tool
def search_tool(query: str) -> str:
    """联网搜索工具，根据用户问题搜索相关信息。"""
    return web_search(query) or "搜索不可用"