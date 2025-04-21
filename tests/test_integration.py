import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from unittest.mock import patch
from integration import get_and_save_weather  # ← без "src."
import logging
import time

class TestIntegrationWeather(unittest.TestCase):
    def setUp(self):
        self.api_key = "fake_key"

    @patch("integration.save_weather_to_db")
    @patch("integration.get_weather")
    def test_successful_get_and_save(self, mock_get, mock_save):
        mock_get.return_value = {
            "city": "Almaty",
            "temperature": 12.5,
            "description": "ясно"
        }

        result = get_and_save_weather("Almaty", self.api_key)
        self.assertTrue(result)
        mock_get.assert_called_once_with("Almaty", self.api_key)
        mock_save.assert_called_once_with("Almaty", 12.5, "ясно")

    @patch("integration.get_weather")
    def test_network_error_logs(self, mock_get):
        mock_get.side_effect = Exception("Ошибка сети")

        logging.shutdown()
        if os.path.exists("error.log"):
            os.remove("error.log")

        result = get_and_save_weather("Almaty", self.api_key)
        self.assertFalse(result)

        time.sleep(0.1)

        self.assertTrue(os.path.exists("error.log"))
        with open("error.log", "r", encoding="utf-8") as f:
            logs = f.read()
            self.assertIn("Ошибка при получении и сохранении погоды", logs)

if __name__ == "__main__":
    unittest.main()
