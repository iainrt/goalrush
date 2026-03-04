from django.db import transaction
from django.core.exceptions import ValidationError
from .models import League, LeagueMembership
import uuid


class LeagueService:

    @staticmethod
    @transaction.atomic
    def join_league_by_join_code(*, user, join_code: str):

        join_code = (join_code or "").strip().upper()
        if not join_code:
            raise ValidationError("Join code is required.")

        league = League.objects.select_for_update().filter(join_code=join_code).first()
        if not league:
            raise ValidationError("Invalid join code.")

        if league.is_locked:
            raise ValidationError("This league is locked and cannot accept new members.")

        # Prevent duplicates
        if LeagueMembership.objects.filter(user=user, league=league).exists():
            raise ValidationError("You are already a member of this league.")

        LeagueMembership.objects.create(
            user=user,
            league=league,
            role="member"
        )

        return league
    
    @staticmethod
    @transaction.atomic
    def regenerate_join_code(*, user, league):
        # only league admins
        if not LeagueMembership.objects.filter(user=user, league=league, role="admin").exists():
            raise ValidationError("Only league admins can regenerate the join code.")

        while True:
            code = uuid.uuid4().hex[:10].upper()
            if not League.objects.filter(join_code=code).exists():
                league.join_code = code
                league.save(update_fields=["join_code"])
                return league.join_code