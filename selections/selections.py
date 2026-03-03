from .models import Pick

class PickSelector:

    @staticmethod
    def user_picks_for_gameweek(user, league, gameweek):
        return Pick.objects.filter(user=user, league=league, gameweek=gameweek)

    @staticmethod
    def league_picks_for_gameweek(league, gameweek):
        return Pick.objects.filter(league=league, gameweek=gameweek)