import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def validate_forecast_date(date_str: str) -> datetime.date:
    """
    Проверяет корректность формата даты и диапазон значения.

    Формат даты должен быть 'dd.MM.yyyy'.
    Дата не может быть в прошлом и не может быть больше чем через 10 дней от сегодня.

    Args:
        date_str (str): Дата в формате строки 'dd.MM.yyyy'.

    Returns:
        datetime.date: Объект даты, если проверка прошла успешно.

    Raises:
        ValueError: При неверном формате даты или выходе за допустимый диапазон.
    """
    try:
        date = datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError:
        logger.error(f"Неверный формат даты: {date_str}. Ожидается 'dd.MM.yyyy'.")
        raise ValueError("Неверный формат даты, используйте dd.MM.yyyy")

    today = datetime.today().date()
    if date < today:
        logger.error(f"Дата в прошлом: {date_str}")
        raise ValueError("Дата не может быть в прошлом")
    if date > today + timedelta(days=10):
        logger.error(f"Дата слишком далеко в будущем: {date_str}")
        raise ValueError("Дата не может быть в будущем больше, чем на 10 дней от текущей")

    logger.debug(f"Дата {date_str} успешно валидирована.")
    return date
