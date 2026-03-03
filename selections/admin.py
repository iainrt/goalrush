from django.contrib import admin
from .models import UserSelection, Pick

@admin.register(UserSelection)
class UserSelectionAdmin(admin.ModelAdmin):
    list_display = ("user", "gameweek", "match", "created_at")
    list_filter = ("gameweek",)
    search_fields = ("user__username",)

@admin.register(Pick)
class PickAdmin(admin.ModelAdmin):
    list_display = ("user", "league", "gameweek", "match", "result_status", "created_at")
    list_filter = ("league", "gameweek", "result_status")
    search_fields = ("user__username", "match__home_team__name", "match__away_team__name")
    autocomplete_fields = ("user", "league", "gameweek", "match")