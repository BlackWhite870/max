import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Добавляем хендлер только если его ещё нет
if not logger.handlers:
    file_handler = logging.FileHandler("error.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def get_weather(city: str, api_key: str) -> dict:
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != 200:
            logger.error(f"Ошибка API: {data}")
            raise ValueError(data.get("message", "Ошибка при получении данных"))

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP ошибка: {http_err}")
        if response.status_code == 401:
            raise ValueError("Неверный API-ключ.")
        elif response.status_code == 404:
            raise ValueError("Город не найден.")
        else:
            raise ValueError(f"HTTP ошибка: {http_err}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка сети. Проверьте подключение к интернету. {e}")
        raise ValueError("Ошибка сети. Проверьте подключение к интернету.")
