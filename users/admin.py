from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("screen_name", "is_admin", "user")
    list_filter = ("is_admin",)
    search_fields = ("screen_name", "user__username")