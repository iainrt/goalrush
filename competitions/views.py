from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from django.views.decorators.http import require_POST

from .forms import JoinLeagueForm, LeagueCreateForm
from .models import League, LeagueMembership
from .services import LeagueService

from gameweeks.models import Gameweek
from selections.models import Pick


@login_required
def join_league(request):
    form = JoinLeagueForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        join_code = form.cleaned_data["join_code"]
        try:
            league = LeagueService.join_league_by_join_code(
                user=request.user,
                join_code=join_code
            )
            messages.success(request, f"You joined: {league.name}")
            return redirect("league_detail", league_id=league.id)
        except ValidationError as e:
            messages.error(request, str(e))

    return render(request, "competitions/join_league.html", {"form": form})


@login_required
def league_list(request):
    leagues = (
        League.objects
        .filter(memberships__user=request.user)
        .select_related("season", "created_by")
        .annotate(member_count=Count("memberships", distinct=True))
        .order_by("-created_at")
    )

    return render(request, "competitions/league_list.html", {"leagues": leagues})


@login_required
def league_create(request):
    form = LeagueCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        league = form.save(commit=False)
        league.created_by = request.user
        league.save()
        messages.success(request, f"League created: {league.name}")
        return redirect("league_detail", league_id=league.id)

    return render(request, "competitions/league_create.html", {"form": form})


@login_required
def league_detail(request, league_id: int):
    league = get_object_or_404(
        League.objects.select_related("season", "created_by"),
        id=league_id,
    )

    membership = LeagueMembership.objects.filter(user=request.user, league=league).first()
    if not membership:
        raise PermissionDenied("You are not a member of this league.")

    is_admin = membership.role == "admin"

    members = (
        LeagueMembership.objects
        .filter(league=league)
        .select_related("user")
        .order_by("-role", "joined_at")
    )

    latest_gw = (
        Gameweek.objects
        .filter(league=league, published=True)
        .prefetch_related("competitions")
        .order_by("-start_date")
        .first()
    )

    picks = []
    if latest_gw:
        picks = (
            Pick.objects
            .filter(league=league, gameweek=latest_gw)
            .select_related("user", "match", "match__home_team", "match__away_team")
            .order_by("created_at")
        )

    return render(
        request,
        "competitions/league_detail.html",
        {
            "league": league,
            "membership": membership,
            "is_admin": is_admin,
            "members": members,
            "latest_gw": latest_gw,
            "picks": picks,
        },
    )


@login_required
@require_POST
def league_lock(request, league_id):
    try:
        league = LeagueService.lock_league(user=request.user, league_id=league_id)
        messages.success(request, f"{league.name} is now locked.")
    except (PermissionDenied, ValidationError) as e:
        messages.error(request, str(e))
    return redirect("league_detail", league_id=league_id)


@login_required
@require_POST
def league_unlock(request, league_id):
    try:
        league = LeagueService.unlock_league(user=request.user, league_id=league_id)
        messages.success(request, f"{league.name} is now unlocked.")
    except (PermissionDenied, ValidationError) as e:
        messages.error(request, str(e))
    return redirect("league_detail", league_id=league_id)


@login_required
@require_POST
def league_remove_member(request, league_id, user_id):
    try:
        LeagueService.remove_member(
            user=request.user,
            league_id=league_id,
            member_user_id=user_id,
        )
        messages.success(request, "Member removed.")
    except (PermissionDenied, ValidationError) as e:
        messages.error(request, str(e))
    return redirect("league_detail", league_id=league_id)


@login_required
@require_POST
def league_regenerate_code(request, league_id):
    try:
        new_code = LeagueService.regenerate_join_code(
            user=request.user,
            league_id=league_id,
        )
        messages.success(request, f"New join code: {new_code}")
    except (PermissionDenied, ValidationError) as e:
        messages.error(request, str(e))

    return redirect("league_detail", league_id=league_id)