from datetime import timedelta

from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator, RegexValidator
from django.db import models
from django.db.models import Q, F
from django.utils.timezone import now
#make migrations i migrate fer quan acabi str, i editar lo de la pull request
class Map(models.Model):
    MapType = models.TextChoices("MapType", "Small Medium Large")
    map_id = models.AutoField(primary_key=True)
    map_name = models.CharField(max_length=50)
    creator = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=MapType)
    dimensions = models.DecimalField(decimal_places=2, validators=[MinValueValidator(2)])

    def __str__(self):
        return self.map_name

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=50)

    def __str__(self):
        return self.country_name

class WebUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(validators=[EmailValidator()])
    password = models.CharField(max_length=200)
    user_country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="country_users")

    def __str__(self):
        return self.username

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    reviewer = models.ForeignKey(WebUser, on_delete=models.SET_NULL, related_name="reviews_written", null=True)
    reviewer_name = models.CharField(max_length=50)
    reviewee = models.ForeignKey(WebUser, on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["reviewer", "reviewee"],name="unique_reviewer_reviewee"),
                       models.CheckConstraint(check=~Q(reviewer=F("reviewee")),name="check_no_self_reviews")]

    def __str__(self):
        return f"From {self.reviewer_name} to {self.reviewee.username}: {self.title}"

class CounterUser(models.Model):
    user = models.OneToOneField(WebUser, on_delete=models.CASCADE, related_name="corresponding_CS_user", primary_key=True)
    favourite_map = models.ForeignKey(Map, on_delete=models.SET_NULL, null=True, blank=True)
    wins = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    losses = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    kills = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    deaths = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    score = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.user.username}: {self.score}"

class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    players = models.ManyToManyField(CounterUser, through="MatchStats")
    winner = models.ForeignKey(CounterUser, on_delete=models.SET_NULL, null=True)
    winner_name = models.CharField(max_length=50)
    score_display = models.CharField(max_length=20, validators=[RegexValidator(regex=r"^\d+-\d+$")])
    duration = models.DurationField(validators=[MinValueValidator(timedelta(0))])
    date = models.DateField(validators=[MaxValueValidator(now)])

    def __str__(self):
        return f"Winner: {self.winner_name}, result: {self.score_display}"

class MatchStats(models.Model):
    match_stats_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CounterUser, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=50)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    kills = models.IntegerField(validators=[MinValueValidator(0)])
    deaths = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "match"], condition=Q(user__isnull=False),name="unique_user_match")]

    def __str__(self):
        return f"{self.username}: {self.kills} kills, {self.deaths} deaths"

class GlobalRanking(models.Model):
    global_ranking_id = models.AutoField(primary_key=True)
    counter_user = models.OneToOneField(CounterUser, on_delete=models.CASCADE, related_name="corresponding_global_ranking", unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="country_counter_users")
    global_position = models.IntegerField(unique=True, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"User: {self.counter_user.user.username}: Score {self.counter_user.score}, Position {self.global_position}"

class LocalRanking(models.Model):
    local_ranking_id = models.AutoField(primary_key=True)
    counter_user = models.OneToOneField(CounterUser, on_delete=models.CASCADE, related_name="corresponding_local_ranking", unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="country_counter_users")
    local_position = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["country", "local_position"],name="unique_country_ranking")]

    def __str__(self):
        return f"{self.counter_user.user.username}: Score {self.counter_user.score}, Position ({self.country.country_name}) {self.local_position}"
