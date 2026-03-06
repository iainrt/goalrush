from django.contrib import admin
from .models import Season, Competition, League, LeagueMembership


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    search_fields = ("name",)


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "api_league_id")
    search_fields = ("name", "country")


class LeagueMembershipInline(admin.TabularInline):
    model = LeagueMembership
    extra = 0
    autocomplete_fields = ("user",)


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ("name", "season", "created_by", "is_public", "is_locked")
    search_fields = ("name", "created_by__username", "join_code")
    list_filter = ("season", "is_public", "is_locked")
    autocomplete_fields = ("created_by", "season")
    inlines = [LeagueMembershipInline]


@admin.register(LeagueMembership)
class LeagueMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "league", "role", "joined_at")
    list_filter = ("role", "league")
    autocomplete_fields = ("user", "league")