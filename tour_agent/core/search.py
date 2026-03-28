import requests
from core.config import BOCHA_API_KEY, BOCHA_SEARCH_URL


def web_search(query: str, limit=5):
    if not BOCHA_API_KEY or not BOCHA_SEARCH_URL:
        return {"error": "搜索服务配置不完整，请检查环境变量 BOCHA_API_KEY 和 BOCHA_SEARCH_URL"}

    headers = {"Authorization": f"Bearer {BOCHA_API_KEY}"}
    data = {
        "query": query,
        "count": limit,
        "summary": True  # 长摘要，适合AI
    }
    try:
        res = requests.post(
            BOCHA_SEARCH_URL,
            headers=headers,
            json=data,
            timeout=15
        ).json()

        code = res.get("code")
        if code not in (0, "0", "200", 200):
            return {"error": f"搜索API返回错误: {res.get('message', code)}"}

        results = res.get("data", {}).get("webPages", {}).get("value", [])
        if not results:
            return {"error": "未找到相关搜索结果"}

        return [
            {
                "title": item.get("name"),
                "snippet": item.get("summary") or (item.get("snippet") or "")[:300]
            }
            for item in results[:limit]
        ]
    except requests.exceptions.Timeout:
        return {"error": "搜索请求超时，请稍后重试"}
    except requests.exceptions.ConnectionError:
        return {"error": "搜索服务连接失败，请检查网络或API服务"}
    except Exception as e:
        return {"error": f"搜索异常: {str(e)}"}
