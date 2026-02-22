from django.contrib import admin
from .models import Season, Competition

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    list_editable = ("active",)
    search_fields = ("name",)

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "api_league_id")
    search_fields = ("name", "country")