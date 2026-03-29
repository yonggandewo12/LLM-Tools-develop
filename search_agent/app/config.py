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

SEARCH_ENGINE = os.getenv("SEARCH_ENGINE", "tavily").lower()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_MAX_RESULTS = int(os.getenv("TAVILY_MAX_RESULTS", 5))
SEARXNG_API_URL = os.getenv("SEARXNG_API_URL")
SEARXNG_MAX_RESULTS = int(os.getenv("SEARXNG_MAX_RESULTS", 5))