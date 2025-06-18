from django.db import models


class ForecastOverride(models.Model):
    """
    Модель для хранения переопределенных прогнозов погоды.

    Используется для хранения пользовательских прогнозов, которые
    имеют приоритет над данными из внешнего API.

    Ограничения:
    - Город хранится в нижнем регистре
    - Минимальная температура не может быть больше максимальной
    - Комбинация города и даты должна быть уникальной
    """

    city = models.CharField(max_length=100)
    date = models.DateField()
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()

    class Meta:
        unique_together = ("city", "date")
        indexes = [
            models.Index(fields=["city", "date"]),
        ]

    def __str__(self):
        return f"{self.city} - {self.date}"

    def save(self, *args, **kwargs):
        self.city = self.city.lower()
        super().save(*args, **kwargs)
