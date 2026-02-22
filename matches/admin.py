from django.contrib import admin
from .models import Team, Match

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "competition", "api_team_id")
    list_filter = ("competition",)
    search_fields = ("name",)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "home_team",
        "away_team",
        "competition",
        "kickoff_time",
        "status",
        "home_goals",
        "away_goals",
        "both_scored",
    )
    list_filter = ("competition", "status", "season")
    search_fields = ("home_team__name", "away_team__name")