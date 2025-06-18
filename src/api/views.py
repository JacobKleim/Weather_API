import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.services import WeatherService
from utils.decorators import external_api_error_handler

from .serializers import (
    CurrentWeatherGetSerializer,
    ForecastGetSerializer,
    ForecastOverrideSerializer,
)

logger = logging.getLogger(__name__)


class CurrentWeatherView(APIView):
    """
    Представление для получения текущей погоды в городе.

    Возвращает текущую температуру и локальное время.
    """

    @external_api_error_handler
    def get(self, request):
        """
        GET /api/weather/current

        Query-параметры:
            city (str): Название города на английском языке

        Returns:
            Response: JSON с текущей температурой и локальным временем
            {
                "temperature": float,  # Текущая температура в градусах Цельсия
                "local_time": str     # Локальное время в формате HH:mm
            }

        Status codes:
            200: Успешный ответ
            400: Ошибка валидации параметров
            503: Ошибка внешнего API
        """
        serializer = CurrentWeatherGetSerializer(data=request.query_params)
        if not serializer.is_valid():
            logger.warning(f"CurrentWeatherView: Ошибка валидации параметров: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        city = serializer.validated_data["city"]
        service = WeatherService(city)
        data = service.get_current_weather()

        return Response(data, status=status.HTTP_200_OK)


class ForecastWeatherView(APIView):
    """
    Представление для работы с прогнозом погоды.

    Поддерживает:
    - GET: получение прогноза на конкретную дату
    - POST: переопределение прогноза для конкретной даты
    """

    @external_api_error_handler
    def get(self, request):
        """
        GET /api/weather/forecast

        Query-параметры:
            city (str): Название города на английском языке
            date (str): Дата в формате dd.MM.yyyy

        Returns:
            Response: JSON с минимальной и максимальной температурой
            {
                "min_temperature": float,  # Минимальная температура
                "max_temperature": float   # Максимальная температура
            }

        Status codes:
            200: Успешный ответ
            400: Ошибка валидации параметров
            503: Ошибка внешнего API
        """
        serializer = ForecastGetSerializer(data=request.query_params)
        if not serializer.is_valid():
            logger.warning(f"ForecastWeatherView GET: Ошибка валидации: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        city = serializer.validated_data["city"]
        date = serializer.validated_data["date"]

        service = WeatherService(city)
        data = service.get_forecast_for_date(date)

        return Response(data, status=status.HTTP_200_OK)

    @external_api_error_handler
    def post(self, request):
        """
        POST /api/weather/forecast

        Позволяет задать или переопределить прогноз погоды для указанного города на дату.
        Если прогноз для данной даты и города уже существует, он будет перезаписан.

        Body (JSON):
            {
                "city": str,           # Название города
                "date": str,           # Дата в формате dd.MM.yyyy
                "min_temperature": float,  # Минимальная температура
                "max_temperature": float   # Максимальная температура
            }

        Returns:
            Response: JSON с сохраненными данными прогноза

        Status codes:
            201: Прогноз успешно создан/обновлен
            400: Ошибка валидации данных
            503: Ошибка внешнего API
        """
        serializer = ForecastOverrideSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"ForecastWeatherView POST: Ошибки валидации: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        city = serializer.validated_data["city"]
        service = WeatherService(city)
        override = service.update_forecast_override(serializer.validated_data)

        logger.info(f"ForecastWeatherView POST: Обновлен прогноз для '{city}' на '{override.date}', кеш очищен.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
