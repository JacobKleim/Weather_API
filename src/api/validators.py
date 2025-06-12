import logging
from datetime import date, timedelta
from rest_framework import serializers

logger = logging.getLogger(__name__)


def validate_forecast_date(value: date) -> date:
    """
    Проверяет диапазон значения даты.
    Дата не может быть в прошлом и не может быть больше чем через 10 дней от сегодня.

    Args:
        value (date): Дата для проверки

    Returns:
        date: Объект даты, если проверка прошла успешно

    Raises:
        serializers.ValidationError: При выходе за допустимый диапазон дат
    """
    today = date.today()
    if value < today:
        logger.warning(f"Дата прогноза {value} в прошлом.")
        raise serializers.ValidationError("Дата не может быть в прошлом.")
    if value > today + timedelta(days=10):
        logger.warning(f"Дата прогноза {value} слишком далеко в будущем.")
        raise serializers.ValidationError("Дата не может быть больше, чем через 10 дней.")
    return value


def validate_temperatures(min_temp: float | None, max_temp: float | None) -> None:
    """
    Проверяет корректность значений минимальной и максимальной температуры.

    Args:
        min_temp (float | None): Минимальная температура
        max_temp (float | None): Максимальная температура

    Raises:
        serializers.ValidationError: Если минимальная температура выше максимальной
    """
    if min_temp is not None and max_temp is not None and min_temp > max_temp:
        logger.error(f"Некорректные значения температуры: min={min_temp}, max={max_temp}")
        raise serializers.ValidationError("Минимальная температура не может быть выше максимальной.")
