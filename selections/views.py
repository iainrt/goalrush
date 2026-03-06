from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from competitions.models import League, LeagueMembership
from gameweeks.models import Gameweek
from matches.models import Match
from .forms import PickMatchesForm
from .models import Pick
from .services import PickService


@login_required
def pick_matches(request, league_id):
    league = get_object_or_404(League, id=league_id)

    membership = LeagueMembership.objects.filter(user=request.user, league=league).first()
    if not membership:
        raise PermissionDenied("You are not a member of this league.")

    gameweek = (
        Gameweek.objects
        .filter(league=league, published=True, locked=False)
        .prefetch_related("competitions")
        .order_by("start_date")
        .first()
    )

    if not gameweek:
        messages.error(request, "No open published gameweek is available for this league.")
        return redirect("league_detail", league_id=league.id)

    user_picks = Pick.objects.filter(
        user=request.user,
        league=league,
        gameweek=gameweek,
    ).select_related("match", "match__home_team", "match__away_team")

    taken_match_ids = Pick.objects.filter(
        league=league,
        gameweek=gameweek,
    ).values_list("match_id", flat=True)

    available_matches = (
        Match.objects
        .filter(
            season=league.season,
            competition__in=gameweek.competitions.all(),
            kickoff_time__gte=gameweek.start_date,
            kickoff_time__lte=gameweek.end_date,
        )
        .exclude(id__in=taken_match_ids)
        .select_related("home_team", "away_team", "competition")
        .order_by("kickoff_time")
    )

    other_picks = (
        Pick.objects
        .filter(league=league, gameweek=gameweek)
        .exclude(user=request.user)
        .select_related("user", "match", "match__home_team", "match__away_team")
        .order_by("created_at")
    )

    form = PickMatchesForm(
        request.POST or None,
        available_matches=available_matches,
    )

    if request.method == "POST":
        if user_picks.exists():
            messages.error(request, "You have already submitted picks for this gameweek.")
            return redirect("pick_matches", league_id=league.id)

        if form.is_valid():
            try:
                PickService.create_two_picks(
                    user=request.user,
                    league=league,
                    gameweek=gameweek,
                    matches=form.cleaned_data["match_ids"],
                )
                messages.success(request, "Your picks have been submitted.")
                return redirect("pick_matches", league_id=league.id)
            except (ValidationError, ValueError) as e:
                messages.error(request, str(e))

    return render(
        request,
        "selections/pick_matches.html",
        {
            "league": league,
            "gameweek": gameweek,
            "form": form,
            "available_matches": available_matches,
            "user_picks": user_picks,
            "other_picks": other_picks,
        },
    )