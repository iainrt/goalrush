from django.db import models
from django.utils import timezone
from django.db.models import UniqueConstraint
from competitions.models import Season, Competition, League


class Gameweek(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="gameweeks")
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    number = models.IntegerField(null=True, blank=True)

    competitions = models.ManyToManyField(Competition, related_name="gameweeks")

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    published = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    lock_time = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["league", "name"],
                name="unique_gameweek_name_per_league"
            )
        ]
        indexes = [
            models.Index(fields=["league"]),
            models.Index(fields=["season"]),
            models.Index(fields=["published"]),
            models.Index(fields=["locked"]),
            models.Index(fields=["lock_time"]),
        ]

    def __str__(self):
        return f"{self.league.name} - {self.name}"

    def should_lock(self):
        return bool(self.lock_time and timezone.now() >= self.lock_time)