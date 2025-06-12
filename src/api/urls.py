from django.urls import path

from .views import CurrentWeatherView, ForecastWeatherView

urlpatterns = [
    path("weather/current", CurrentWeatherView.as_view(), name="current-weather"),
    path("weather/forecast", ForecastWeatherView.as_view(), name="forecast-weather"),
]
