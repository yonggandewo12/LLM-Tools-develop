from dotenv import load_dotenv
import os

load_dotenv()

# LLM
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))

# 国内搜索
BOCHA_API_KEY = os.getenv("BOCHA_API_KEY")
BOCHA_SEARCH_URL = os.getenv("BOCHA_SEARCH_URL")

# 国内天气
QWEATHER_API_KEY = os.getenv("QWEATHER_API_KEY")
QWEATHER_URL = os.getenv("QWEATHER_URL")
