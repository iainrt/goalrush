from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Season(models.Model):
    name = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Competition(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    api_league_id = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.country})"


# =========================
# User League (social league)
# =========================
class League(models.Model):
    name = models.CharField(max_length=120)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_leagues")

    join_code = models.CharField(max_length=12, unique=True)
    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["season", "competition"]),
            models.Index(fields=["join_code"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.competition.name})"