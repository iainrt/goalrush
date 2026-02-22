from django.db import models
from competitions.models import Season

class Gameweek(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    published = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return self.name