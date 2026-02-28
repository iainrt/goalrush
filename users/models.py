from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    screen_name = models.CharField(max_length=50, unique=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.screen_name


# =========================
# League Membership
# =========================
class LeagueMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey("competitions.League", on_delete=models.CASCADE, related_name="members")

    is_admin = models.BooleanField(default=False)  # league admin
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "league"], name="unique_user_per_league")
        ]

    def __str__(self):
        return f"{self.user.username} in {self.league.name}"