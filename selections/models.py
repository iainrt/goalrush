from django.db import models
from django.contrib.auth.models import User
from matches.models import Match
from gameweeks.models import Gameweek

class UserSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gameweek = models.ForeignKey(Gameweek, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['gameweek', 'match'], name='unique_match_per_gameweek'),
            models.UniqueConstraint(fields=['user', 'gameweek', 'match'], name='unique_user_pick')
        ]