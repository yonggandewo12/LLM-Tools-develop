from langchain_openai import ChatOpenAI
from app.config import (
    LLM_BASE_URL,
    LLM_MODEL,
    LLM_API_KEY,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS
)

def _normalize_base_url(url: str) -> str:
    """Remove /chat/completions suffix if present to avoid 404 errors"""
    normalized = url.rstrip("/")
    if normalized.endswith("/chat/completions"):
        normalized = normalized[:-len("/chat/completions")]
    return normalized

def get_llm():
    return ChatOpenAI(
        base_url=_normalize_base_url(LLM_BASE_URL),
        api_key=LLM_API_KEY,
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
        streaming=True,
        timeout=30
    )
