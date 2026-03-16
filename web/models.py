from asyncio.windows_events import NULL

from django.core.validators import MinValueValidator
from django.db import models

MAP_CHOISES

class Map(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.CharField(max_length=100)
    dimensions = models.FloatField(validators=[MinValueValidator(2)])


class CounterUser(models.Model):
    id = models.AutoField(primary_key=True)
    favourite_map = models.ForeignKey(Map, default=NULL)
    win = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    loses = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    kills = models.FloatField(default=0, validators=[MinValueValidator(0)])
    deaths = models.FloatField(default=0, validators=[MinValueValidator(0)])


