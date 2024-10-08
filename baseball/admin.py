from django.contrib import admin
from .models import BaseballStats


class BaseballStatsAdmin(admin.ModelAdmin):
    list_display = ("player", "rank", "hits", "year", "age", "bats")
    list_filter = ("bats", )

admin.site.register(BaseballStats, BaseballStatsAdmin)


