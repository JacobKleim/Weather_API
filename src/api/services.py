import logging

from django.core.cache import cache

from api.models import ForecastOverride
from api.weather_provider.weatherbit import fetch_current_weather, fetch_forecast
from project import settings

logger = logging.getLogger(__name__)

CURRENT_WEATHER_CACHE_TIMEOUT = settings.CURRENT_WEATHER_CACHE_TIMEOUT
FORECAST_WEATHER_CACHE_TIMEOUT = settings.FORECAST_WEATHER_CACHE_TIMEOUT


class WeatherService:
    """
    Сервис для работы с погодными данными.

    Предоставляет методы для:
    - Получения текущей погоды
    - Получения прогноза на конкретную дату
    - Переопределения прогноза
    """

    def __init__(self, city: str):
        """
        Инициализация сервиса.

        Args:
            city (str): Название города на английском языке
        """
        self.city = city.lower()

    def get_current_weather(self):
        """
        Получает текущую погоду в городе.

        Сначала проверяет кеш, если данных нет - запрашивает из API.

        Returns:
            dict: {
                "temperature": float,  # Текущая температура в градусах Цельсия
                "local_time": str     # Локальное время в формате HH:mm
            }

        Raises:
            ValueError: Если город не найден или произошла ошибка при обращении к API
        """
        cache_key = f"current_weather:{self.city}"
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"[WeatherService] Ответ по {self.city}: из кеша")
            return cached

        data = fetch_current_weather(self.city)
        cache.set(cache_key, data, timeout=CURRENT_WEATHER_CACHE_TIMEOUT)
        logger.info(f"[WeatherService] Ответ по {self.city}: с API")
        return data

    def get_forecast_for_date(self, date):
        """
        Получает прогноз погоды на конкретную дату.

        Проверяет данные в следующем порядке:
        1. Кеш
        2. Переопределенный прогноз из БД
        3. Внешний API

        Args:
            date (date): Дата прогноза

        Returns:
            dict: {
                "min_temperature": float,  # Минимальная температура
                "max_temperature": float   # Максимальная температура
            }

        Raises:
            ValueError: Если прогноз не найден или произошла ошибка при обращении к API
        """
        cache_key = f"forecast:{self.city}:{date.isoformat()}"
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"[WeatherService] Ответ по {self.city}: из кеша")
            return cached

        override = ForecastOverride.objects.filter(city=self.city, date=date).first()
        if override:
            data = {
                "min_temperature": override.min_temperature,
                "max_temperature": override.max_temperature,
            }
            cache.set(cache_key, data, timeout=FORECAST_WEATHER_CACHE_TIMEOUT)
            logger.info(f"[WeatherService] Ответ по {self.city}: из БД")
            return data

        forecast_data = fetch_forecast(self.city, date.strftime("%Y-%m-%d"))
        cache.set(cache_key, forecast_data, timeout=FORECAST_WEATHER_CACHE_TIMEOUT)
        logger.info(f"[WeatherService] Ответ по {self.city}: с API")
        return forecast_data

    def update_forecast_override(self, validated_data):
        """
        Обновляет или создает переопределение прогноза погоды.

        После обновления данных очищает кеш для данного прогноза.

        Args:
            validated_data (dict): Валидированные данные прогноза
                {
                    "city": str,
                    "date": date,
                    "min_temperature": float,
                    "max_temperature": float
                }

        Returns:
            ForecastOverride: Объект переопределения прогноза
        """
        city = validated_data["city"].lower()
        date = validated_data["date"]

        override, _ = ForecastOverride.objects.update_or_create(
            city=city,
            date=date,
            defaults={
                "min_temperature": validated_data["min_temperature"],
                "max_temperature": validated_data["max_temperature"],
            },
        )
        cache_key = f"forecast:{self.city}:{date.isoformat()}"
        cache.delete(cache_key)
        return override
