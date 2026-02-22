from django.db import models

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