import requests
from datetime import timedelta
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, MinLengthValidator
from django.db import models, transaction
from django.db.models import Q, F, Max
from django.db.models.functions import Coalesce
from django.utils.timezone import now
from web.services.rankings import update_global_ranking, update_local_ranking

DEFAULT_COUNTRY = 9
WIN_MODE = 1

class Map(models.Model):
    MapType = models.TextChoices("MapType", "Small Big")
    map_id = models.AutoField(primary_key=True)
    map_name = models.CharField(max_length=50)
    creator = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=MapType)
    dimensions = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(2)])

    def __str__(self):
        return self.map_name

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_iso = models.CharField(unique=True, max_length=2, validators=[RegexValidator(regex=r"^[A-Z]{2}$")])
    country_name = models.CharField(unique=True, max_length=50)
    flag_image = models.ImageField(upload_to="country_flags/", blank=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.country_name}-{self.country_iso}"

    @staticmethod
    def get_default_country():
        return DEFAULT_COUNTRY

    def get_flag_image(self):
        url = f"https://flagcdn.com/{self.country_iso.lower()}.svg"
        for _ in range(5):
            response = requests.get(url)
            if response.status_code == 200:
                previous = self.flag_image
                self.flag_image.save(f"{self.country_iso}.svg", ContentFile(response.content), save=True)
                break

class WebUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, validators=[UnicodeUsernameValidator(), MinLengthValidator(3)])
    email = models.EmailField(unique=True, validators=[RegexValidator(r"^[^@]+@gmail\.com$")])
    user_country = models.ForeignKey(Country, on_delete=models.SET_DEFAULT, related_name="country_users", blank=True, null=True, default=Country.get_default_country())
    user_image = models.ImageField(upload_to="user_images/", blank=True)

    class Meta:
        verbose_name = "WebUser"
        verbose_name_plural = "WebUsers"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.pk is None:
            if not self.user_country_id:
                self.user_country_id = Country.get_default_country()
            super().save(*args, **kwargs)
            CounterUser.objects.create(user=self)
            return
        user = WebUser.objects.get(pk=self.pk)
        old_country_id, old_username = user.user_country_id, user.username
        super().save(*args, **kwargs)
        if old_country_id != self.user_country_id:
            self.update_rankings_countries(old_country_id)
        elif old_username != self.username:
            self.update_matches_reviews_username()

    def update_rankings_countries(self, old_country_id):
        cs_user = self.corresponding_CS_user
        new_country_id = self.user_country.country_id
        global_ranking, local_ranking = cs_user.corresponding_global_ranking, cs_user.corresponding_local_ranking
        global_ranking.country_id, local_ranking.country_id = new_country_id, new_country_id
        global_ranking.save()
        local_ranking.local_position = None
        local_ranking.save()
        update_local_ranking(old_country_id)
        update_local_ranking(new_country_id)

    def update_matches_reviews_username(self):
        cs_user = self.corresponding_CS_user
        Review.objects.filter(reviewer_id=cs_user.pk).update(reviewer_name=self.username)
        for match in Match.objects.filter(Q(winner_id=self.pk)|Q(loser_id=self.pk)).prefetch_related("matches_match_stats"):
            match.update_match_usernames(match.winner_id == cs_user.pk, cs_user.pk, self.username)

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
    favourite_map = models.ForeignKey(Map, default=None, on_delete=models.SET_NULL, null=True)
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

    def save(self, *args, **kwargs):
        is_new = self._state.adding is True
        super().save(*args, **kwargs)
        if is_new:
            country = self.user.user_country
            with transaction.atomic():
                global_position = GlobalRanking.objects.aggregate(max_position=Coalesce(Max("global_position"), 0))["max_position"] + 1
                local_position = LocalRanking.objects.filter(country=country).aggregate(max_position=Coalesce(Max("local_position"), 0))["max_position"] + 1
                GlobalRanking.objects.create(counter_user=self, country=country, global_position=global_position)
                LocalRanking.objects.create(counter_user=self, country=country, local_position=local_position)

    def update_parameters(self, stats, mode):
        self.score += stats.points
        self.kills += stats.kills
        self.deaths += stats.deaths
        if mode == WIN_MODE:
            self.wins += 1
        else:
            self.losses += 1
        self.save()
        update_global_ranking()
        update_local_ranking(self.user.user_country_id)

class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    loser = models.ForeignKey(CounterUser, related_name= "matches_lost", on_delete=models.SET_NULL, null=True)
    loser_name = models.CharField(max_length=50)
    winner = models.ForeignKey(CounterUser, related_name= "matches_won", on_delete=models.SET_NULL, null=True)
    winner_name = models.CharField(max_length=50)
    score_display = models.CharField(max_length=5, validators=[RegexValidator(regex=r"^(10-[0-9]|[0-9]-10)$")])
    duration = models.DurationField(validators=[MinValueValidator(timedelta(0))])
    date = models.DateTimeField(validators=[MaxValueValidator(now)])
    log_file = models.FileField(upload_to="match_logs/", null=True)

    class Meta:
        constraints = [models.CheckConstraint(condition=~Q(winner=F("loser")),name="winner_cannot_be_loser")]
        verbose_name_plural = "Matches"

    def __str__(self):
        return f"{self.winner_name} vs {self.loser_name}: {self.score_display} - {self.date}"

    def update_match_usernames(self, mode, user_id, new_username):
        if mode == WIN_MODE:
            self.winner_name = new_username
        else:
            self.loser_name = new_username
        self.save()
        self.matches_match_stats.filter(user_id=user_id).update(username=new_username)

class MatchStats(models.Model):
    match_stats_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CounterUser, related_name= "users_match_stats", on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=50)
    match = models.ForeignKey(Match, related_name= "matches_match_stats", on_delete=models.CASCADE)
    kills = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    deaths = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    points = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "match"], condition=Q(user__isnull=False),name="unique_user_match")]
        verbose_name_plural = "MatchStats"

    def __str__(self):
        return f"{self.username}-{self.match.date}: {self.kills} kills, {self.deaths} deaths, {self.points} points"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.user.update_parameters(self, self.points > 0)

    def clean(self):
        is_winner = (self.user_id == self.match.winner_id)
        if is_winner and self.points <= 0:
            raise ValidationError("Winner's score must increase after winning.")
        if not is_winner and self.points > 0:
            raise ValidationError("Loser's score mustn't increase after losing.")
        if self.points + self.user.score < 0:
            raise ValidationError("Any user's score should always remain positive.")

class GlobalRanking(models.Model):
    global_ranking_id = models.AutoField(primary_key=True)
    counter_user = models.OneToOneField(CounterUser, on_delete=models.CASCADE, related_name="corresponding_global_ranking")
    country = models.ForeignKey(Country, on_delete=models.SET_DEFAULT, related_name="global_country_counter_users", default=Country.get_default_country())
    global_position = models.IntegerField(unique=True, validators=[MinValueValidator(1)], null=True)

    class Meta:
        verbose_name = "GlobalRanking"
        verbose_name_plural = "GlobalRankings"

    def __str__(self):
        return f"User: {self.counter_user.user.username}, Score: {self.counter_user.score}, Position: {self.global_position}"

class LocalRanking(models.Model):
    local_ranking_id = models.AutoField(primary_key=True)
    counter_user = models.OneToOneField(CounterUser, on_delete=models.CASCADE, related_name="corresponding_local_ranking")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name="local_country_counter_users", null=True)
    local_position = models.IntegerField(validators=[MinValueValidator(1)], null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["country", "local_position"],name="unique_country_ranking")]
        verbose_name = "LocalRanking"
        verbose_name_plural = "LocalRankings"

    def __str__(self):
        return f"User: {self.counter_user.user.username}, Score: {self.counter_user.score}, Position ({self.country.country_name}): {self.local_position}"