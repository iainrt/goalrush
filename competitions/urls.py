from django.urls import path
from .views import join_league

urlpatterns = [
    path("leagues/join/", join_league, name="join_league"),
]