from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from competitions.models import LeagueMembership
from .models import Gameweek


class GameweekService:
    @staticmethod
    def _require_league_admin(*, user, league):
        membership = LeagueMembership.objects.filter(user=user, league=league).first()
        if not membership:
            raise PermissionDenied("You are not a member of this league.")
        if membership.role != "admin":
            raise PermissionDenied("Only league admins can manage gameweeks.")

    @staticmethod
    @transaction.atomic
    def create_gameweek(
        *,
        user,
        league,
        name,
        number,
        season,
        competitions,
        start_date,
        end_date,
        lock_time,
        published=False,
        locked=False,
    ):
        GameweekService._require_league_admin(user=user, league=league)

        if season != league.season:
            raise ValidationError("Gameweek season must match the league season.")

        if start_date >= end_date:
            raise ValidationError("Start date must be before end date.")

        if lock_time and lock_time > start_date:
            raise ValidationError("Lock time should be on or before the first fixture window start.")

        gameweek = Gameweek.objects.create(
            league=league,
            season=season,
            name=name,
            number=number,
            start_date=start_date,
            end_date=end_date,
            lock_time=lock_time,
            published=published,
            locked=locked,
        )
        gameweek.competitions.set(competitions)

        return gameweek