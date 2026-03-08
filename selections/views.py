from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from competitions.models import League, LeagueMembership
from gameweeks.models import Gameweek
from matches.models import Match
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
        .filter(
            league=league,
            published=True,
            locked=False,
        )
        .prefetch_related("competitions")
        .order_by("-start_date")
        .first()
    )

    if not gameweek:
        messages.error(request, "No published and unlocked gameweek is available for this league.")
        return redirect("league_detail", league_id=league.id)

    user_picks = (
        Pick.objects
        .filter(user=request.user, league=league, gameweek=gameweek)
        .select_related("user", "match", "match__home_team", "match__away_team", "match__competition")
        .order_by("created_at")
    )

    all_picks = (
        Pick.objects
        .filter(league=league, gameweek=gameweek)
        .select_related("user", "match", "match__home_team", "match__away_team", "match__competition")
    )

    taken_match_ids = set(all_picks.values_list("match_id", flat=True))
    user_pick_ids = set(user_picks.values_list("match_id", flat=True))

    # match_id -> username
    taken_by_map = {pick.match_id: pick.user.username for pick in all_picks}

    matches = (
        Match.objects
        .filter(
            season=league.season,
            competition__in=gameweek.competitions.all(),
            kickoff_time__gte=gameweek.start_date,
            kickoff_time__lte=gameweek.end_date,
        )
        .select_related("home_team", "away_team", "competition")
        .order_by("competition__name", "kickoff_time")
    )

    grouped_matches = OrderedDict()
    for match in matches:
        competition_name = match.competition.name
        grouped_matches.setdefault(competition_name, []).append(match)

    other_picks = (
        all_picks
        .exclude(user=request.user)
        .order_by("created_at")
    )

    if request.method == "POST":
        selected_ids = request.POST.getlist("match_ids")

        if user_picks.exists():
            messages.error(request, "You have already submitted picks for this gameweek.")
            return redirect("pick_matches", league_id=league.id)

        if len(selected_ids) != 2:
            messages.error(request, "You must choose exactly 2 matches.")
            return redirect("pick_matches", league_id=league.id)

        matches = list(
            Match.objects.filter(
                id__in=selected_ids,
                season=league.season,
                competition__in=gameweek.competitions.all(),
                kickoff_time__gte=gameweek.start_date,
                kickoff_time__lte=gameweek.end_date,
            )
        )

        if len(matches) != 2:
            messages.error(request, "Invalid matches selected.")
            return redirect("pick_matches", league_id=league.id)

        if any(match.id in taken_match_ids for match in matches):
            messages.error(request, "One or more selected matches have already been taken.")
            return redirect("pick_matches", league_id=league.id)

        try:
            PickService.create_two_picks(
                user=request.user,
                league=league,
                gameweek=gameweek,
                matches=matches,
            )
            messages.success(request, "Your picks have been submitted.")
            return redirect("pick_matches", league_id=league.id)
        except (ValidationError, ValueError) as e:
            messages.error(request, str(e))
            return redirect("pick_matches", league_id=league.id)

    return render(
        request,
        "selections/pick_matches.html",
        {
            "league": league,
            "gameweek": gameweek,
            "grouped_matches": grouped_matches,
            "user_picks": user_picks,
            "other_picks": other_picks,
            "taken_match_ids": taken_match_ids,
            "user_pick_ids": user_pick_ids,
            "taken_by_map": taken_by_map,
        },
    )