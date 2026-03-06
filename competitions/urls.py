from django.urls import path
from .views import join_league, league_list, league_create, league_detail

urlpatterns = [
    path("leagues/", league_list, name="league_list"),
    path("leagues/create/", league_create, name="league_create"),
    path("leagues/<int:league_id>/", league_detail, name="league_detail"),
    path("leagues/join/", join_league, name="join_league"),
]