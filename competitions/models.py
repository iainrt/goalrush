from django.conf import settings
from django.db import models
import uuid

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


class League(models.Model):
    name = models.CharField(max_length=120)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_leagues"
    )

    join_code = models.CharField(max_length=12, unique=True, blank=True)
    is_public = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["season"]),
            models.Index(fields=["join_code"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "season"],
                name="unique_league_per_season"
            )
        ]

    def __str__(self):
        return self.name

    def _generate_join_code(self):
        return uuid.uuid4().hex[:10].upper()

    def save(self, *args, **kwargs):
        if not self.join_code:
            while True:
                code = self._generate_join_code()
                if not League.objects.filter(join_code=code).exists():
                    self.join_code = code
                    break

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            LeagueMembership.objects.create(
                user=self.created_by,
                league=self,
                role="admin"
            )


class LeagueMembership(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("member", "Member"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "league")

    def __str__(self):
        return f"{self.user} in {self.league.name}"