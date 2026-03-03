from django.db import models
from django.contrib.auth.models import User
from matches.models import Match
from gameweeks.models import Gameweek
from django.conf import settings
from django.db.models import UniqueConstraint

User = settings.AUTH_USER_MODEL

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

class Pick(models.Model):

    RESULT_STATUS = [
        ("pending", "Pending"),
        ("btts_success", "BTTS Success"),
        ("btts_fail", "BTTS Fail"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="picks")
    league = models.ForeignKey("competitions.League", on_delete=models.CASCADE, related_name="picks")
    gameweek = models.ForeignKey("gameweeks.Gameweek", on_delete=models.CASCADE, related_name="picks")

    match = models.ForeignKey("matches.Match", on_delete=models.CASCADE, related_name="picks")

    result_status = models.CharField(max_length=20, choices=RESULT_STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Only one user can pick a match per league per gameweek
            models.UniqueConstraint(
                fields=["league", "gameweek", "match"],
                name="unique_match_per_league_gameweek"
            ),

            # Prevent same user picking same match twice
            models.UniqueConstraint(
                fields=["user", "league", "gameweek", "match"],
                name="unique_pick_per_user_match"
            ),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.match}"