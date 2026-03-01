from django.contrib import admin
from .models import Season, Competition, League

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    list_editable = ("active",)
    search_fields = ("name",)

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "api_league_id")
    search_fields = ("name", "country")

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ("name", "competition", "season", "is_public", "created_at")
    search_fields = ("name", "join_code")
    list_filter = ("competition", "season")