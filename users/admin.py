from django.contrib import admin
from .models import UserProfile, LeagueMembership

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("screen_name", "is_admin", "user")
    list_filter = ("is_admin",)
    search_fields = ("screen_name", "user__username")

admin.register(LeagueMembership)
class LeagueMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "league", "is_admin", "joined_at")
    list_filter = ("league", "is_admin")