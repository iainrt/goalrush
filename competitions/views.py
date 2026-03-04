from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from .services import LeagueService


@login_required
def join_league_view(request, code):
    try:
        league = LeagueService.join_league_by_code(
            user=request.user,
            code=code
        )
        messages.success(request, f"You joined {league.name}")
    except ValidationError as e:
        messages.error(request, str(e))

    return redirect("dashboard")  # change to your actual page

# Create your views here.
