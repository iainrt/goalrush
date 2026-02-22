from django.db import models
from competitions.models import Competition, Season

class Team(models.Model):
    name = models.CharField(max_length=100)
    api_team_id = models.IntegerField(unique=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Match(models.Model):
    api_fixture_id = models.IntegerField(unique=True)

    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_matches")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_matches")

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    kickoff_time = models.DateTimeField()
    status = models.CharField(max_length=30)

    home_goals = models.IntegerField(null=True, blank=True)
    away_goals = models.IntegerField(null=True, blank=True)

    both_scored = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"