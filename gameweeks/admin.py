from django.contrib import admin
from .models import Gameweek


@admin.register(Gameweek)
class GameweekAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "competition",
        "season",
        "start_date",
        "end_date",
        "lock_time",
        "published",
        "locked",
    )

    list_editable = ("published", "locked")

    list_filter = ("season", "competition", "published", "locked")

    ordering = ("competition", "start_date")

    search_fields = ("name",)

    readonly_fields = ("created_at",)