from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from .forms import JoinLeagueForm
from .services import LeagueService


@login_required
def join_league(request):
    if request.method == "POST":
        form = JoinLeagueForm(request.POST)
        if form.is_valid():
            try:
                league = LeagueService.join_league_by_join_code(
                    user=request.user,
                    join_code=form.cleaned_data["join_code"]
                )
                messages.success(request, f"You joined {league.name}")
                return redirect("league_detail", league_id=league.id)
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = JoinLeagueForm()

    return render(request, "competitions/join_league.html", {"form": form})