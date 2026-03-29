from dotenv import load_dotenv
import os

load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")
LLM_API_KEY = os.getenv("LLM_API_KEY", "dummy")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.1))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 2048))

# 搜索引擎配置（当前固定为DuckDuckGo）
SEARCH_ENGINE = os.getenv("SEARCH_ENGINE", "duckduckgo").lower()

# DuckDuckGo搜索配置
DDG_REGION = os.getenv("DDG_REGION", "zh-cn")
DDG_MAX_RESULTS = int(os.getenv("DDG_MAX_RESULTS", 5))
DDG_TIMEOUT = int(os.getenv("DDG_TIMEOUT", 10))

# 记忆配置
MEMORY_MAX_MESSAGES = int(os.getenv("MEMORY_MAX_MESSAGES", 10))