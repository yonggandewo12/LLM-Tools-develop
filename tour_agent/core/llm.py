from langchain_openai import ChatOpenAI
from core.config import *


def _normalize_openai_base_url(url: str | None) -> str | None:
    if not url:
        return url

    normalized = url.rstrip("/")
    suffix = "/chat/completions"
    if normalized.endswith(suffix):
        normalized = normalized[: -len(suffix)]

    return normalized

# 函数名统一为：get_local_llm
def get_local_llm():
    return ChatOpenAI(
        openai_api_base=_normalize_openai_base_url(LLM_BASE_URL),
        model_name=LLM_MODEL,
        openai_api_key=LLM_API_KEY,
        temperature=LLM_TEMPERATURE,
        request_timeout=60
    )
