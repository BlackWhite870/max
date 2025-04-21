import unittest
from unittest.mock import patch
import os
import logging
import time
import sys

# Добавляем путь к src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import weather_api  # теперь импорт работает точно

class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        self.api_key = "fake_key"

    @patch("weather_api.requests.get")
    def test_successful_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "name": "Almaty",
            "main": {"temp": 12.5},
            "weather": [{"description": "ясно"}],
            "cod": 200
        }

        result = weather_api.get_weather("Almaty", self.api_key)
        self.assertEqual(result["city"], "Almaty")
        self.assertEqual(result["temperature"], 12.5)
        self.assertEqual(result["description"], "ясно")

    @patch("weather_api.requests.get")
    def test_city_not_found(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"cod": "404", "message": "city not found"}
        mock_get.return_value.raise_for_status.side_effect = weather_api.requests.exceptions.HTTPError("404")

        with self.assertRaises(ValueError) as context:
            weather_api.get_weather("UnknownCity", self.api_key)
        self.assertIn("Город не найден", str(context.exception))

    @patch("weather_api.requests.get")
    def test_network_error_logs(self, mock_get):
        mock_get.side_effect = weather_api.requests.exceptions.RequestException("Ошибка соединения")

        # Удаляем лог, если есть
        logging.shutdown()
        if os.path.exists("error.log"):
            os.remove("error.log")

        # Вызываем ошибку
        with self.assertRaises(ValueError):
            weather_api.get_weather("Almaty", self.api_key)

        # Даём логгеру время на запись
        time.sleep(0.1)

        self.assertTrue(os.path.exists("error.log"), "Файл error.log не создан")

        with open("error.log", "r", encoding="utf-8") as f:
            logs = f.read()
            self.assertIn("Ошибка сети", logs)

if __name__ == '__main__':
    unittest.main()
