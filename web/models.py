import requests

from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.db.models import Q, F
from django.utils.timezone import now
from django.core.files.base import ContentFile

DEFAULT_COUNTRY = 1

class Map(models.Model):
    MapType = models.TextChoices("MapType", "Small Medium Large")
    map_id = models.AutoField(primary_key=True)
    map_name = models.CharField(max_length=50)
    creator = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=MapType)
    dimensions = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(2)])

    def __str__(self):
        return self.map_name

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_iso = models.CharField(unique=True, max_length=2, validators=[RegexValidator(regex=r"^[A-Z]{2}$")])
    country_name = models.CharField(max_length=50)
    flag_image = models.ImageField(upload_to="country_flags/", blank=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.country_name}-{self.country_iso}"

    @staticmethod
    def get_default_country():
        return DEFAULT_COUNTRY

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.flag_image:
            self.get_flag_image()

    def get_flag_image(self):
        response = requests.get(f"https://flagsapi.com/{self.country_iso}/flat/64.png")
        for _ in range(3):
            if response.status_code == 200:
                self.flag_image.save(f"{self.country_iso}.png", ContentFile(response.content), save=True)
                return

class WebUser(AbstractUser):
    email = models.EmailField(unique=True, validators=[RegexValidator(r"^[^@]+@gmail\.com$")])
    user_country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="country_users", default=Country.get_default_country())
    user_image = models.ImageField(upload_to="user_images/", blank=True)

    class Meta:
        verbose_name = "WebUser"
        verbose_name_plural = "WebUsers"

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
                       models.CheckConstraint(condition=~Q(reviewer=F("reviewee")),name="check_no_self_reviews")]

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

    class Meta:
        verbose_name = "CounterUser"
        verbose_name_plural = "CounterUsers"

    def __str__(self):
        return self.user.username

class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    loser = models.ForeignKey(CounterUser, related_name= "matches_lost", on_delete=models.SET_NULL, null=True)
    loser_name = models.CharField(max_length=50)
    winner = models.ForeignKey(CounterUser, related_name= "matches_won", on_delete=models.SET_NULL, null=True)
    winner_name = models.CharField(max_length=50)
    score_display = models.CharField(max_length=20, validators=[RegexValidator(regex=r"^\d+-\d+$")])
    duration = models.DurationField(validators=[MinValueValidator(timedelta(0))])
    date = models.DateTimeField(validators=[MaxValueValidator(now)])

    class Meta:
        constraints = [models.CheckConstraint(condition=~Q(winner=F("loser")),name="winner_cannot_be_loser")]
        verbose_name_plural = "Matches"

    def __str__(self):
        return f"{self.winner_name} vs {self.loser_name}: {self.score_display} - {self.date}"

class MatchStats(models.Model):
    match_stats_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CounterUser, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=50)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    kills = models.IntegerField(validators=[MinValueValidator(0)])
    deaths = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "match"], condition=Q(user__isnull=False),name="unique_user_match")]
        verbose_name_plural = "MatchStats"

    def __str__(self):
        return f"{self.username}-{self.match.date}: {self.kills} kills, {self.deaths} deaths"

class GlobalRanking(models.Model):
    global_ranking_id = models.AutoField(primary_key=True)
    counter_user = models.OneToOneField(CounterUser, on_delete=models.CASCADE, related_name="corresponding_global_ranking")
    global_position = models.IntegerField(unique=True, validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "GlobalRanking"
        verbose_name_plural = "GlobalRankings"

    def __str__(self):
        return f"User: {self.counter_user.user.username}, Score: {self.counter_user.score}, Position: {self.global_position}"

class LocalRanking(models.Model):
    local_ranking_id = models.AutoField(primary_key=True)
    counter_user = models.OneToOneField(CounterUser, on_delete=models.CASCADE, related_name="corresponding_local_ranking")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="local_country_counter_users")
    local_position = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["country", "local_position"],name="unique_country_ranking")]
        verbose_name = "LocalRanking"
        verbose_name_plural = "LocalRankings"

    def __str__(self):
        return f"User: {self.counter_user.user.username}, Score: {self.counter_user.score}, Position ({self.country.country_name}): {self.local_position}"

    def save(self, *args, **kwargs):
        self.country = self.counter_user.user.user_country
        super().save(*args, **kwargs)