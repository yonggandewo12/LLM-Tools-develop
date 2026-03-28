import requests
from core.config import QWEATHER_API_KEY, QWEATHER_URL


CITY_CODE_MAP = {
    "北京": "101010100",
    "上海": "101020100",
    "广州": "101280100",
    "深圳": "101280600",
    "成都": "101270100",
    "杭州": "101210100",
    "南京": "101190100",
    "西安": "101110100",
    "重庆": "101040100",
    "武汉": "101200100",
    "苏州": "101190400",
    "天津": "101030100",
}


def get_weather(city: str):
    if not QWEATHER_API_KEY or not QWEATHER_URL:
        return {"error": "天气服务配置不完整，请检查环境变量 QWEATHER_API_KEY 和 QWEATHER_URL"}

    location = CITY_CODE_MAP.get(city, city)

    try:
        res = requests.get(
            QWEATHER_URL,
            params={
                "location": location,
                "key": QWEATHER_API_KEY
            },
            timeout=10,
            proxies={"http": None, "https": None}
        ).json()

        code = res.get("code")
        if code == "200":
            now = res.get("now", {})
            return {
                "city": city,
                "weather": now.get("text", "未知"),
                "temp": now.get("temp", "N/A"),
                "feelsLike": now.get("feelsLike", "N/A"),
                "windDir": now.get("windDir", "未知"),
                "humidity": now.get("humidity", "N/A")
            }
        else:
            return {"error": f"天气查询失败: {res.get('error', {}).get('detail', res)}"}
    except requests.exceptions.Timeout:
        return {"error": "天气请求超时，请稍后重试"}
    except requests.exceptions.ConnectionError:
        return {"error": "天气服务连接失败，请检查网络或API服务"}
    except Exception as e:
        return {"error": f"请求异常: {str(e)}"}
