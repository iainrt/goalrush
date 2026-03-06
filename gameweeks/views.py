from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from competitions.models import League, LeagueMembership
from .forms import GameweekCreateForm
from .models import Gameweek
from .services import GameweekService


@login_required
def league_gameweek_list(request, league_id):
    league = get_object_or_404(League, id=league_id)

    membership = LeagueMembership.objects.filter(user=request.user, league=league).first()
    if not membership:
        raise PermissionDenied("You are not a member of this league.")

    gameweeks = (
        Gameweek.objects
        .filter(league=league)
        .prefetch_related("competitions")
        .order_by("-start_date")
    )

    return render(
        request,
        "gameweeks/league_gameweek_list.html",
        {
            "league": league,
            "gameweeks": gameweeks,
            "is_admin": membership.role == "admin",
        },
    )


@login_required
def league_gameweek_create(request, league_id):
    league = get_object_or_404(League, id=league_id)

    membership = LeagueMembership.objects.filter(user=request.user, league=league).first()
    if not membership or membership.role != "admin":
        raise PermissionDenied("Only league admins can create gameweeks.")

    form = GameweekCreateForm(request.POST or None, league=league)

    if request.method == "POST" and form.is_valid():
        try:
            gameweek = GameweekService.create_gameweek(
                user=request.user,
                league=league,
                name=form.cleaned_data["name"],
                number=form.cleaned_data["number"],
                season=league.season,
                competitions=form.cleaned_data["competitions"],
                start_date=form.cleaned_data["start_date"],
                end_date=form.cleaned_data["end_date"],
                lock_time=form.cleaned_data["lock_time"],
                published=form.cleaned_data["published"],
                locked=form.cleaned_data["locked"],
            )
            messages.success(request, f"Gameweek created: {gameweek.name}")
            return redirect("league_gameweek_list", league_id=league.id)
        except (PermissionDenied, ValidationError) as e:
            messages.error(request, str(e))

    return render(
        request,
        "gameweeks/league_gameweek_create.html",
        {
            "league": league,
            "form": form,
            "is_edit": False,
        },
    )


@login_required
def league_gameweek_edit(request, league_id, gameweek_id):
    league = get_object_or_404(League, id=league_id)
    gameweek = get_object_or_404(Gameweek, id=gameweek_id, league=league)

    membership = LeagueMembership.objects.filter(user=request.user, league=league).first()
    if not membership or membership.role != "admin":
        raise PermissionDenied("Only league admins can edit gameweeks.")

    if gameweek.locked:
        messages.error(request, "Locked gameweeks cannot be edited. Unlock it first.")
        return redirect("league_gameweek_list", league_id=league.id)

    form = GameweekCreateForm(request.POST or None, instance=gameweek, league=league)

    if request.method == "POST" and form.is_valid():
        try:
            GameweekService.update_gameweek(
                user=request.user,
                gameweek=gameweek,
                name=form.cleaned_data["name"],
                number=form.cleaned_data["number"],
                competitions=form.cleaned_data["competitions"],
                start_date=form.cleaned_data["start_date"],
                end_date=form.cleaned_data["end_date"],
                lock_time=form.cleaned_data["lock_time"],
                published=form.cleaned_data["published"],
                locked=form.cleaned_data["locked"],
            )
            messages.success(request, f"Gameweek updated: {gameweek.name}")
            return redirect("league_gameweek_list", league_id=league.id)
        except (PermissionDenied, ValidationError) as e:
            messages.error(request, str(e))

    return render(
        request,
        "gameweeks/league_gameweek_create.html",
        {
            "league": league,
            "form": form,
            "gameweek": gameweek,
            "is_edit": True,
        },
    )


@login_required
@require_POST
def league_gameweek_publish(request, league_id, gameweek_id):
    league = get_object_or_404(League, id=league_id)
    gameweek = get_object_or_404(Gameweek, id=gameweek_id, league=league)

    try:
        GameweekService.publish_gameweek(user=request.user, gameweek=gameweek)
        messages.success(request, f"{gameweek.name} published.")
    except (PermissionDenied, ValidationError) as e:
        messages.error(request, str(e))

    return redirect("league_gameweek_list", league_id=league.id)


@login_required
@require_POST
def league_gameweek_unpublish(request, league_id, gameweek_id):
    league = get_object_or_404(League, id=league_id)
    gameweek = get_object_or_404(Gameweek, id=gameweek_id, league=league)

    try:
        GameweekService.unpublish_gameweek(user=request.user, gameweek=gameweek)
        messages.success(request, f"{gameweek.name} unpublished.")
    except (PermissionDenied, ValidationError) as e:
        messages.error(request, str(e))

    return redirect("league_gameweek_list", league_id=league.id)


@login_required
@require_POST
def league_gameweek_lock(request, league_id, gameweek_id):
    league = get_object_or_404(League, id=league_id)
    gameweek = get_object_or_404(Gameweek, id=gameweek_id, league=league)

    try:
        GameweekService.lock_gameweek(user=request.user, gameweek=gameweek)
        messages.success(request, f"{gameweek.name} locked.")
    except (PermissionDenied, ValidationError) as e:
        messages.error(request, str(e))

    return redirect("league_gameweek_list", league_id=league.id)


@login_required
@require_POST
def league_gameweek_unlock(request, league_id, gameweek_id):
    league = get_object_or_404(League, id=league_id)
    gameweek = get_object_or_404(Gameweek, id=gameweek_id, league=league)

    try:
        GameweekService.unlock_gameweek(user=request.user, gameweek=gameweek)
        messages.success(request, f"{gameweek.name} unlocked.")
    except (PermissionDenied, ValidationError) as e:
        messages.error(request, str(e))

    return redirect("league_gameweek_list", league_id=league.id)