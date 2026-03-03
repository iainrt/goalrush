from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Count

from .models import Pick
from users.models import LeagueMembership
from gameweeks.models import Gameweek
from matches.models import Match


class PickValidator:

    @staticmethod
    def validate_user_in_league(user, league):
        if not LeagueMembership.objects.filter(user=user, league=league).exists():
            raise ValidationError("User is not a member of this league.")

    @staticmethod
    def validate_gameweek(gameweek: Gameweek):
        if not gameweek.published:
            raise ValidationError("Gameweek is not published.")
        if gameweek.locked:
            raise ValidationError("Gameweek is locked.")
        if gameweek.lock_time and timezone.now() >= gameweek.lock_time:
            raise ValidationError("Gameweek is locked.")

    @staticmethod
    def validate_pick_limit(user, league, gameweek, limit=2):
        count = Pick.objects.filter(
            user=user,
            league=league,
            gameweek=gameweek
        ).count()

        if count >= limit:
            raise ValidationError(f"Maximum {limit} picks allowed per gameweek.")

    @staticmethod
    def validate_match(match: Match, gameweek: Gameweek, league):
        # Match belongs to same competition
        if match.competition_id != gameweek.competition_id:
            raise ValidationError("Match not in this competition.")

        # Match in time window
        if not (gameweek.start_date <= match.kickoff <= gameweek.end_date):
            raise ValidationError("Match not in this gameweek window.")

        # Match not already picked in league
        if Pick.objects.filter(
            league=league,
            gameweek=gameweek,
            match=match
        ).exists():
            raise ValidationError("This match has already been picked by another user.")

