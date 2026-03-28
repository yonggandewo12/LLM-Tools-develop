from langchain_openai import ChatOpenAI
from app.config import (
    LLM_BASE_URL,
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS
)

def get_llm():
    return ChatOpenAI(
        base_url=LLM_BASE_URL,
        api_key="dummy",
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
        streaming=True
    )