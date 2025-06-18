from rest_framework import serializers

from .models import ForecastOverride
from .validators import validate_forecast_date, validate_temperatures


class ForecastOverrideSerializer(serializers.ModelSerializer):
    date = serializers.DateField(
        required=True,
        input_formats=["%d.%m.%Y", "%Y-%m-%d"],
        help_text=(
            "Дата прогноза в формате ДД.ММ.ГГГГ или ISO YYYY-MM-DD. "
            "Не может быть в прошлом и не может быть больше, чем через 10 дней от текущей даты."
        ),
    )
    min_temperature = serializers.FloatField(
        required=True,
        help_text=("Минимальная температура в градусах Цельсия. Должна быть не выше максимальной температуры."),
    )
    max_temperature = serializers.FloatField(
        required=True,
        help_text=("Максимальная температура в градусах Цельсия. Должна быть не ниже минимальной температуры."),
    )

    class Meta:
        model = ForecastOverride
        fields = "__all__"

    def validate_date(self, value):
        """
        Валидирует дату.
        Проверяет, что дата не в прошлом и не дальше 10 дней в будущем.
        """
        return validate_forecast_date(value)

    def validate(self, data):
        """
        Проверяет корректность взаимосвязи между минимальной и максимальной температурой.
        """
        validate_temperatures(data.get("min_temperature"), data.get("max_temperature"))
        return data


class ForecastGetSerializer(serializers.Serializer):
    city = serializers.CharField(
        required=True,
        help_text="Название города на английском языке (например: Moscow, Amsterdam)",
    )
    date = serializers.DateField(
        required=True,
        input_formats=["%d.%m.%Y", "%Y-%m-%d"],
        help_text=(
            "Дата прогноза в формате ДД.ММ.ГГГГ или ISO YYYY-MM-DD. "
            "Не может быть в прошлом и не может быть больше, чем через 10 дней от текущей даты."
        ),
    )

    def validate_date(self, value):
        """
        Валидирует дату.
        Проверяет, что дата не в прошлом и не дальше 10 дней в будущем.
        """
        return validate_forecast_date(value)


class CurrentWeatherGetSerializer(serializers.Serializer):
    city = serializers.CharField(
        required=True,
        help_text="Название города на английском языке (например: Moscow, Amsterdam)",
    )
