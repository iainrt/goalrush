from django.contrib import admin
from .models import UserSelection

@admin.register(UserSelection)
class UserSelectionAdmin(admin.ModelAdmin):
    list_display = ("user", "gameweek", "match", "created_at")
    list_filter = ("gameweek",)
    search_fields = ("user__username",)