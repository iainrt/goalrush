from django.urls import path
from .views import pick_matches

urlpatterns = [
    path("leagues/<int:league_id>/picks/", pick_matches, name="pick_matches"),
]