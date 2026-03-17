# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Player Profile
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.nickname


# Route (Meru → Nairobi segments)
class Route(models.Model):
    name = models.CharField(max_length=100)
    distance_km = models.FloatField()

    def __str__(self):
        return self.name


# Pickup / Drop points
class Checkpoint(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location_km = models.FloatField()  # distance from start

    def __str__(self):
        return f"{self.name} ({self.route.name})"


# Game Session (one race)
class GameSession(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    time_taken = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.nickname} - {self.route.name}"