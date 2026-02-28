from django.db import models
from django.utils import timezone
from django.db.models import UniqueConstraint
from competitions.models import Season, Competition


class Gameweek(models.Model):
    name = models.CharField(max_length=50)  # e.g. "GW1", "Matchday 12"

    number = models.IntegerField(null=True, blank=True)  # optional numeric index

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    # Locking + publishing
    published = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    lock_time = models.DateTimeField(null=True, blank=True)

    # Scope
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["season", "competition", "name"],
                name="unique_gameweek_per_competition_season"
            )
        ]

        indexes = [
            models.Index(fields=["season", "competition"]),
            models.Index(fields=["published"]),
            models.Index(fields=["locked"]),
            models.Index(fields=["lock_time"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.competition.name}"

    def should_lock(self):
        if not self.lock_time:
            return False
        return timezone.now() >= self.lock_time