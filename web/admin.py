from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *

# Arreglar tema de rankings de admin, quan tingui la lògica de ranking fer que el camp de ranking quedi amagat en creacio.

admin.site.unregister(Group)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_iso')
    list_editable = ('country_iso',)
    list_per_page = 20
    ordering = ('country_name',)
    search_fields = ('country_name', 'country_iso')

@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('map_name', 'creator', 'type', 'dimensions')
    list_editable = ('creator', 'type', 'dimensions')
    list_filter = ('creator', 'type')
    list_per_page = 20
    ordering = ('map_name',)
    search_fields = ('map_name', 'creator', 'type', 'dimensions')

@admin.register(WebUser)
class WebUserAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user_country',)
    list_display = ('username', 'email', 'user_country')
    list_editable = ('email', 'user_country')
    list_filter = ('user_country',)
    list_per_page = 20
    list_select_related = ('user_country',)
    ordering = ('username',)
    search_fields = ('username', 'email', 'user_country__country_name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields = ('reviewer', 'reviewee')
    fields = ('reviewer', 'reviewee', 'rating', 'title', 'description')
    list_display = ('reviewer_display', 'reviewee', 'rating', 'title', 'short_description')
    list_editable = ('rating', 'title')
    list_filter = ('reviewee', 'rating')
    list_per_page = 20
    list_select_related = ('reviewer', 'reviewee',)
    ordering = ('reviewer__username', 'reviewee__username')
    search_fields = ('reviewer__username', 'reviewee__username', 'rating', 'title')

    def get_readonly_fields(self, request, record=None):
        return ('reviewee',) if record else ()

    def save_model(self, request, record, form, change):
        if record.reviewer: record.reviewer_name = record.reviewer.username
        super().save_model(request, record, form, change)

    @admin.display(ordering='reviewer__username', description="Reviewer")
    def reviewer_display(self, record):
        return record.reviewer.username if record.reviewer else f"{record.reviewer_name} (deleted)"

    @admin.display(description="Description")
    def short_description(self, record):
        return (record.description[:20] + "...") if len(record.description) > 20 else record.description

@admin.register(CounterUser)
class CounterUserAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user',)
    list_display = ('user', 'favourite_map', 'wins', 'losses', 'kills', 'deaths', 'score')
    list_editable = ('favourite_map', 'wins', 'losses', 'kills', 'deaths', 'score')
    list_filter = ('favourite_map',)
    list_per_page = 20
    list_select_related = ('user', 'favourite_map',)
    ordering = ('user__username',)
    search_fields = ('user__username', 'favourite_map__map_name', 'score')

    def get_readonly_fields(self, request, record=None):
        return ('user',) if record else ()

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    autocomplete_fields = ('winner', 'loser')
    fields = ('winner', 'loser', 'score_display', 'duration', 'date')
    list_display = ('winner_display', 'loser_display', 'score_display', 'duration', 'date')
    list_filter = ('winner','loser')
    list_per_page = 20
    list_select_related = ('winner', 'winner__user', 'loser', 'loser__user')
    ordering = ('date','winner__user__username', 'loser__user__username')
    search_fields = ('winner__user__username','loser__user__username', 'duration','date')

    def save_model(self, request, record, form, change):
        if record.winner: record.winner_name = record.winner.user.username
        if record.loser: record.loser_name = record.loser.user.username
        super().save_model(request, record, form, change)

    def get_readonly_fields(self, request, record=None):
        return ('winner', 'loser') if record else ()

    @admin.display(ordering='winner__user__username', description="Winner")
    def winner_display(self, record):
        return record.winner.user.username if record.winner else f"{record.winner_name} (deleted)"

    @admin.display(ordering='loser__user__username', description="Loser")
    def loser_display(self, record):
        return record.loser.user.username if record.loser else f"{record.loser_name} (deleted)"


@admin.register(MatchStats)
class MatchStatsAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user', 'match')
    fields = ('user', 'kills', 'match', 'deaths')
    list_display = ('user_display', 'match', 'kills', 'deaths')
    list_filter = ('user',)
    list_per_page = 20
    list_select_related = ('user', 'user__user', 'match')
    ordering = ('match', 'user__user__username')
    search_fields = ('user__user__username', 'match')

    def save_model(self, request, record, form, change):
        if record.user: record.username = record.user.user.username
        super().save_model(request, record, form, change)

    @admin.display(ordering='user__user__username', description="User")
    def user_display(self, record):
        return record.user.user.username if record.user else f"{record.username} (deleted)"

@admin.register(GlobalRanking)
class GlobalRankingAdmin(admin.ModelAdmin):
    autocomplete_fields = ('counter_user',)
    list_display = ('counter_user', 'score', 'country', 'global_position')
    list_filter = ('counter_user__user__user_country',)
    list_per_page = 20
    list_select_related = ('counter_user','counter_user__user', 'counter_user__user__user_country')
    ordering = ('global_position',)
    search_fields = ('counter_user__user__username','counter_user__user__user_country__country_name', 'global_position')

    def get_readonly_fields(self, request, record=None):
        return ('global_position',) if record else ()

    @admin.display(ordering='counter_user__score')
    def score(self, record):
        return record.counter_user.score

    @admin.display(ordering='counter_user__user__user_country__country_name')
    def country(self, record):
        return record.counter_user.user.user_country

@admin.register(LocalRanking)
class LocalRankingAdmin(admin.ModelAdmin):
    autocomplete_fields = ('counter_user',)
    list_display = ('counter_user', 'score', 'country', 'local_position')
    list_filter = ('country',)
    list_per_page = 20
    list_select_related = ('counter_user','counter_user__user')
    ordering = ('country', 'local_position',)
    readonly_fields = ('country',)
    search_fields = ('counter_user__user__username','country__country_name', 'local_position')

    def get_readonly_fields(self, request, record=None):
        return ('local_position','country') if record else ()

    def get_fields(self, request, record=None):
        return ('counter_user', 'local_position') if record is None else ('counter_user', 'country', 'local_position')

    @admin.display(ordering='counter_user__score')
    def score(self, record):
        return record.counter_user.score