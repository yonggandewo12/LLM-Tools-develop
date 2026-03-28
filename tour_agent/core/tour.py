# 这里导入也统一
from core.llm import get_local_llm
from core.search import web_search
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["city", "search_info"],
    template="""
你是旅游推荐助手。
城市：{city}
参考信息：{search_info}

请输出：
1. 必去景点
2. 特色介绍
3. 游玩建议
简洁实用。
"""
)

# 函数名正确
def recommend_attractions(city: str):
    data = web_search(f"{city} 必去旅游景点 最新")
    if not data or isinstance(data, dict):
        return "暂无搜索结果，请稍后重试"
    info_text = "\n".join([item["snippet"] for item in data])
    llm = get_local_llm()
    chain = prompt | llm
    return chain.invoke({"city": city, "search_info": info_text}).content
