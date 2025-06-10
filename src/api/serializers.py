from datetime import datetime, timedelta

from rest_framework import serializers

from .models import ForecastOverride


class ForecastOverrideSerializer(serializers.ModelSerializer):
    date = serializers.DateField(
        required=True,
        input_formats=["%d.%m.%Y", "%Y-%m-%d"],
        help_text="Дата прогноза в формате ДД.ММ.ГГГГ или ISO YYYY-MM-DD.",
    )

    class Meta:
        model = ForecastOverride
        fields = "__all__"

    def validate_date(self, value):
        today = datetime.now().date()
        if value < today:
            raise serializers.ValidationError("Дата не может быть в прошлом.")
        if value > today + timedelta(days=10):
            raise serializers.ValidationError("Дата не может быть больше, чем через 10 дней.")
        return value

    def validate(self, data):
        min_temp = data.get("min_temperature")
        max_temp = data.get("max_temperature")
        if min_temp is not None and max_temp is not None and min_temp > max_temp:
            raise serializers.ValidationError("Минимальная температура не может быть выше максимальной.")
        return data


class ForecastGetSerializer(serializers.Serializer):
    city = serializers.CharField(required=True)
    date = serializers.DateField(
        required=True,
        input_formats=["%d.%m.%Y", "%Y-%m-%d"],
    )

    def validate_date(self, value):
        today = datetime.now().date()
        if value < today:
            raise serializers.ValidationError("Дата не может быть в прошлом.")
        if value > today + timedelta(days=10):
            raise serializers.ValidationError("Дата не может быть больше, чем через 10 дней.")
        return value


class CurrentWeatherGetSerializer(serializers.Serializer):
    city = serializers.CharField(required=True)
