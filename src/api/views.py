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
    @external_api_error_handler
    def get(self, request):
        serializer = CurrentWeatherGetSerializer(data=request.query_params)
        if not serializer.is_valid():
            logger.warning(f"CurrentWeatherView: Ошибка валидации параметров: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        city = serializer.validated_data["city"]
        service = WeatherService(city)
        data = service.get_current_weather()

        return Response(data, status=status.HTTP_200_OK)


class ForecastWeatherView(APIView):
    @external_api_error_handler
    def get(self, request):
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
        serializer = ForecastOverrideSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"ForecastWeatherView POST: Ошибки валидации: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        city = serializer.validated_data["city"]
        service = WeatherService(city)
        override = service.update_forecast_override(serializer.validated_data)

        logger.info(f"ForecastWeatherView POST: Обновлен прогноз для '{city}' на '{override.date}', кеш очищен.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
