from django.contrib import admin
from .models import Gameweek

@admin.register(Gameweek)
class GameweekAdmin(admin.ModelAdmin):
    list_display = ("name", "season", "start_date", "end_date", "published", "locked")
    list_editable = ("published", "locked")
    list_filter = ("season", "published", "locked")