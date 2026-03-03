from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Pick
from .validators import PickValidator


class PickService:

    @staticmethod
    @transaction.atomic
    def create_pick(*, user, league, gameweek, match):
        # Validation chain
        PickValidator.validate_user_in_league(user, league)
        PickValidator.validate_gameweek(gameweek)
        PickValidator.validate_pick_limit(user, league, gameweek)
        PickValidator.validate_match(match, gameweek, league)

        # Create pick
        pick = Pick.objects.create(
            user=user,
            league=league,
            gameweek=gameweek,
            match=match,
        )

        return pick