from django.urls import path
from .views import (
    league_gameweek_list,
    league_gameweek_create,
    league_gameweek_edit,
    league_gameweek_publish,
    league_gameweek_unpublish,
    league_gameweek_lock,
    league_gameweek_unlock,
)

urlpatterns = [
    path("leagues/<int:league_id>/gameweeks/", league_gameweek_list, name="league_gameweek_list"),
    path("leagues/<int:league_id>/gameweeks/create/", league_gameweek_create, name="league_gameweek_create"),
    path("leagues/<int:league_id>/gameweeks/<int:gameweek_id>/edit/", league_gameweek_edit, name="league_gameweek_edit"),
    path("leagues/<int:league_id>/gameweeks/<int:gameweek_id>/publish/", league_gameweek_publish, name="league_gameweek_publish"),
    path("leagues/<int:league_id>/gameweeks/<int:gameweek_id>/unpublish/", league_gameweek_unpublish, name="league_gameweek_unpublish"),
    path("leagues/<int:league_id>/gameweeks/<int:gameweek_id>/lock/", league_gameweek_lock, name="league_gameweek_lock"),
    path("leagues/<int:league_id>/gameweeks/<int:gameweek_id>/unlock/", league_gameweek_unlock, name="league_gameweek_unlock"),
]