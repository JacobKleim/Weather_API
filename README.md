# 🌦 Weather Forecast API — Django Backend

Сервис на Django REST Framework для получения текущей погоды и прогноза, с возможностью переопределения прогноза вручную. Использует внешний API Weatherbit.io и реализует кеширование и идемпотентную логику.

---

## 🚀 Возможности

* Получение текущей погоды по городу
* Получение прогноза на конкретную дату
* Возможность переопределить прогноз на определённую дату
* Приоритет вручную заданных прогнозов над внешними данными
* Кеширование ответов от API и кастомных прогнозов
* Django Admin для управления переопределёнными прогнозами

---

## 🔗 Внешний источник данных

Сервис использует [Weatherbit API](https://www.weatherbit.io/api) для получения текущей погоды и прогноза:

- **Текущая погода:** [`/current`](https://www.weatherbit.io/api/weather-current)
- **Прогноз на дни:** [`/forecast/daily`](https://www.weatherbit.io/api/weather-forecast-16-day)

Для доступа необходим API-ключ, который указывается в переменной окружения `WEATHERBIT_API_KEY`.

---

## 📦 Технологии

* Python 3.12
* Django 5.2.2
* Django REST Framework 3.16.0
* PostgreSQL
* Poetry (управление зависимостями)
* Ruff (статический анализ кода)
* Docker + Docker Compose

---

## ⚙️ Переменные окружения

В `.env` должны быть определены:

```env
DJANGO_SECRET_KEY=django-insecure-key
DJANGO_DEBUG=True

POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=fastapi_password
POSTGRES_DB=fastapi_db

WEATHERBIT_API_KEY=your_api_key_here
WEATHERBIT_URL=https://api.weatherbit.io/v2.0

CURRENT_WEATHER_CACHE_TIMEOUT=300
FORECAST_WEATHER_CACHE_TIMEOUT=900
```

---

## 🐍 Poetry

- Установите pipx и Poetry:
  
   ```bash
   pip install --upgrade pip
   pip install pipx
   pipx install poetry
   ```

- Установка зависимостей:

   ```bash
   poetry install
   ```

---

## 🐳 Docker

- Запуск проекта:

   ```bash
   docker-compose up --build
   ```

- Применение миграций:

   ```bash
   docker-compose exec django python manage.py migrate
   ```

---

## 🔄 Кеширование

- Кеш текущей погоды и прогноза сохраняется по ключам:
  - `current_weather:<city>`
  - `forecast:<city>:<date>`
- Время жизни кеша настраивается в settings (`CURRENT_WEATHER_CACHE_TIMEOUT`, `FORECAST_WEATHER_CACHE_TIMEOUT`).

---

## ✏️ Переопределение прогноза

Для корректировки данных от API можно отправить `POST` с полями `city`, `date`, `min_temperature`, `max_temperature`.  
Они будут иметь приоритет над внешними значениями и сохраняться в модели `ForecastOverride`.

---

## 📁 Структура проекта

- `api/` — основное Django-приложение
- `api/services.py` — бизнес-логика (запросы к API, кеширование)
- `api/serializers.py` — DRF-сериализаторы
- `api/views.py` — вьюхи (REST API)
- `api/models.py` — модель `ForecastOverride`
- `api/validators.py` — валидатор `validate_forecast_date`
- `api/weather_provider/weatherbit.py` — доступ к API Weatherbit

- `src/utils/decorators.py` — декоратор `external_api_error_handler`

---

