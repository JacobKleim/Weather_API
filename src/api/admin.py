from django.contrib import admin

from .models import ForecastOverride


@admin.register(ForecastOverride)
class ForecastOverrideAdmin(admin.ModelAdmin):
    pass
