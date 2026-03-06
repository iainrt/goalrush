from django.urls import path
from .views import league_gameweek_list, league_gameweek_create

urlpatterns = [
    path("leagues/<int:league_id>/gameweeks/", league_gameweek_list, name="league_gameweek_list"),
    path("leagues/<int:league_id>/gameweeks/create/", league_gameweek_create, name="league_gameweek_create"),
]