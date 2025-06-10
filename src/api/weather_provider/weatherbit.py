import requests

from project import settings

API_KEY = settings.WEATHERBIT_API_KEY
BASE_URL = settings.WEATHERBIT_URL


def fetch_current_weather(city: str) -> dict:
    """
    Получает текущую погоду по указанному городу с использованием внешнего API Weatherbit.

    :param city: Название города (строка)
    :return: Словарь с температурой и локальным временем
    :raises ValueError: Если город не найден или API вернул ошибку/невалидные данные
    """
    url = f"{BASE_URL}/current"
    params = {
        "city": city,
        "key": API_KEY,
        "units": "M",
    }
    response = requests.get(url, params=params)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        raise ValueError("Город не найден или произошла ошибка при обращении к внешнему API.")

    try:
        data = response.json()["data"][0]
    except (KeyError, IndexError, ValueError):
        raise ValueError("Некорректный ответ от поставщика погоды.")

    return {
        "temperature": data["temp"],
        "local_time": data["ob_time"][-5:],
    }


def fetch_forecast(city: str, date: str) -> dict:
    """
    Получает прогноз погоды на указанную дату по городу с использованием внешнего API Weatherbit.

    :param city: Название города (строка)
    :param date: Дата в формате YYYY-MM-DD
    :return: Словарь с минимальной и максимальной температурой
    :raises ValueError: Если город или дата не найдены или API вернул ошибку/невалидные данные
    """
    url = f"{BASE_URL}/forecast/daily"
    params = {
        "city": city,
        "key": API_KEY,
        "units": "M",
    }
    response = requests.get(url, params=params)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        raise ValueError("Город не найден или произошла ошибка при обращении к внешнему API.")

    try:
        forecast_data = response.json()["data"]
    except (KeyError, ValueError):
        raise ValueError("Некорректный ответ с прогнозом погоды.")

    for entry in forecast_data:
        if entry.get("datetime") == date:
            return {
                "min_temperature": entry["min_temp"],
                "max_temperature": entry["max_temp"],
            }

    raise ValueError("Прогноз на указанную дату не найден.")
