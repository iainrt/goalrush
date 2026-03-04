from django.db import transaction
from django.core.exceptions import ValidationError

from .models import LeagueInvite, LeagueMembership


class LeagueService:

    @staticmethod
    @transaction.atomic
    def join_league_by_code(*, user, code: str):

        try:
            invite = LeagueInvite.objects.select_for_update().get(code=code)
        except LeagueInvite.DoesNotExist:
            raise ValidationError("Invalid invite code.")

        if not invite.is_valid():
            raise ValidationError("Invite expired or fully used.")

        league = invite.league

        # Prevent duplicate membership
        if LeagueMembership.objects.filter(user=user, league=league).exists():
            raise ValidationError("You are already a member of this league.")

        # Create membership
        LeagueMembership.objects.create(
            user=user,
            league=league,
            role="member"
        )

        # Increment usage safely
        invite.increment_use()

        return league