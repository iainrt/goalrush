from django.db import transaction
from .models import Pick
from .validators import PickValidator


class PickService:

    @staticmethod
    @transaction.atomic
    def create_pick(*, user, league, gameweek, match):
        PickValidator.validate_user_in_league(user, league)
        PickValidator.validate_gameweek(gameweek)
        PickValidator.validate_pick_limit(user, league, gameweek)
        PickValidator.validate_match(match, gameweek, league)

        pick = Pick.objects.create(
            user=user,
            league=league,
            gameweek=gameweek,
            match=match,
        )
        return pick

    @staticmethod
    @transaction.atomic
    def create_two_picks(*, user, league, gameweek, matches):
        matches = list(matches)

        if len(matches) != 2:
            raise ValueError("Exactly 2 matches must be provided.")

        existing_count = Pick.objects.filter(
            user=user,
            league=league,
            gameweek=gameweek,
        ).count()

        if existing_count > 0:
            raise ValueError("You have already submitted picks for this gameweek.")

        created = []
        for match in matches:
            created.append(
                PickService.create_pick(
                    user=user,
                    league=league,
                    gameweek=gameweek,
                    match=match,
                )
            )

        return created