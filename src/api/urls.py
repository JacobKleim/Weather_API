from django.urls import path

from .views import CurrentWeatherView, ForecastWeatherView

urlpatterns = [
    path("weather/current", CurrentWeatherView.as_view()),
    path("weather/forecast", ForecastWeatherView.as_view()),
]
