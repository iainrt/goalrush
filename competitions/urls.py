from django.urls import path
from .views import join_league_view

urlpatterns = [
    path("leagues/join/<str:code>/", join_league_view, name="join_league"),
]