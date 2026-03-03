from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    screen_name = models.CharField(max_length=50, unique=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.screen_name


