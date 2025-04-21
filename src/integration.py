from weather_api import get_weather
from db import save_weather_to_db
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
if not logger.handlers:
    handler = logging.FileHandler("error.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_and_save_weather(city, api_key):
    try:
        weather = get_weather(city, api_key)
        save_weather_to_db(
            weather["city"], weather["temperature"], weather["description"]
        )
        return True
    except Exception as e:
        logger.error(f"Ошибка при получении и сохранении погоды: {e}")
        return False
