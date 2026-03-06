from django.urls import path
from .views import (
    join_league,
    league_list,
    league_create,
    league_detail,
    league_lock,
    league_unlock,
    league_remove_member,
    league_regenerate_code
)

urlpatterns = [
    path("leagues/", league_list, name="league_list"),
    path("leagues/create/", league_create, name="league_create"),
    path("leagues/<int:league_id>/", league_detail, name="league_detail"),
    path("leagues/join/", join_league, name="join_league"),
    path("leagues/<int:league_id>/lock/", league_lock, name="league_lock"),
    path("leagues/<int:league_id>/unlock/", league_unlock, name="league_unlock"),
    path(
        "leagues/<int:league_id>/members/<int:user_id>/remove/",
        league_remove_member,
        name="league_remove_member",
    ),
    path(
        "leagues/<int:league_id>/regenerate-code/",
        league_regenerate_code,
        name="league_regenerate_code",
    ),
]