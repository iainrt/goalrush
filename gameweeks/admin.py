from django.contrib import admin
from .models import Gameweek


@admin.register(Gameweek)
class GameweekAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "league",
        "season",
        "start_date",
        "end_date",
        "lock_time",
        "published",
        "locked",
    )
    list_editable = ("published", "locked")
    list_filter = ("season", "league", "published", "locked")
    search_fields = ("name", "league__name")
    filter_horizontal = ("competitions",)
    readonly_fields = ("created_at",)