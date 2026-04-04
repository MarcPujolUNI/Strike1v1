from datetime import timedelta

from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from django.db import models
from django.db.models import Q, F
from django.utils.timezone import now


class Map(models.Model):
    MapType = models.TextChoices("MapType", "Small Medium Large")
    map_id = models.AutoField(primary_key=True)
    map_name = models.CharField(max_length=50)
    creator = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=MapType)
    dimensions = models.DecimalField(decimal_places=2, validators=[MinValueValidator(2)])

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=50)

class WebUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(validators=[EmailValidator()])
    password = models.CharField(max_length=200)
    user_country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="country_users")

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    reviewer = models.ForeignKey(WebUser, on_delete=models.SET_NULL, related_name="reviews_written", null=True)
    reviewer_name = models.CharField(max_length=50)
    reviewee = models.ForeignKey(WebUser, on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["reviewer", "reviewee"],name="unique_reviewer_reviewee"),
                       models.CheckConstraint(check=~Q(reviewer=F("reviewee")),name="check_no_self_reviews")]

class CounterUser(models.Model):
    user = models.OneToOneField(WebUser, on_delete=models.CASCADE, related_name="corresponding_CS_user", primary_key=True)
    favourite_map = models.ForeignKey(Map, on_delete=models.SET_NULL, null=True, blank=True)
    wins = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    losses = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    kills = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    deaths = models.IntegerField(default=0, validators=[MinValueValidator(0)])

class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    players = models.ManyToManyField(CounterUser, through="MatchStats")
    winner = models.ForeignKey(CounterUser, on_delete=models.SET_NULL, null=True)
    winner_name = models.CharField(max_length=50)
    score_display = models.CharField(max_length=20)
    duration = models.DurationField(validators=[MinValueValidator(timedelta(0))])
    date = models.DateField(validators=[MaxValueValidator(now)])

class MatchStats(models.Model):
    match_stats_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CounterUser, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=50)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    kills = models.IntegerField(validators=[MinValueValidator(0)])
    deaths = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "match"], condition=Q(user__isnull=False),name="unique_user_match")]

class GlobalRanking(models.Model):
    global_ranking_id = models.AutoField(primary_key=True)
    counter_user = models.OneToOneField(CounterUser, on_delete=models.CASCADE, related_name="corresponding_global_ranking", unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="country_counter_users")
    score = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    global_position = models.IntegerField(unique=True, validators=[MinValueValidator(1)])

class LocalRanking(models.Model):
    local_ranking_id = models.AutoField(primary_key=True)
    counter_user = models.OneToOneField(CounterUser, on_delete=models.CASCADE, related_name="corresponding_local_ranking", unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="country_counter_users")
    score = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    local_position = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["country", "local_position"],name="unique_country_ranking")]