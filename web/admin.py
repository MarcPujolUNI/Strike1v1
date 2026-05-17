from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import admin as auth_admin
from web.forms import SignUpForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *

admin.site.unregister(Group)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_iso')
    list_per_page = 10
    ordering = ('country_name',)
    readonly_fields = ('country_name', 'country_iso')
    search_fields = ('country_name', 'country_iso')

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    def has_add_permission(self, request):
        return False

@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('map_name', 'creator', 'type', 'dimensions')
    list_filter = ('creator', 'type')
    list_per_page = 10
    ordering = ('map_name',)
    readonly_fields = ('map_name', 'creator', 'type', 'dimensions')
    search_fields = ('map_name', 'creator', 'type', 'dimensions')

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    def has_add_permission(self, request):
        return False

@admin.register(WebUser)
class WebUserAdmin(auth_admin.UserAdmin):
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('username', 'email', 'password1', 'password2', 'user_country', 'user_image')}),)
    add_form = SignUpForm
    autocomplete_fields = ('user_country',)
    fieldsets = ((None, {'fields': ('username', 'password', 'email', 'user_country', 'user_image')}),('Further options', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined')}),)
    list_display = ('username', 'email', 'user_country')
    list_filter = ('user_country',)
    list_per_page = 10
    list_select_related = ('user_country',)
    ordering = ('username',)
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ('username', 'email', 'user_country__country_name')

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(reverse('admin:web_webuser_changelist'))

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields = ('reviewer', 'reviewee')
    fields = ('reviewer', 'reviewee', 'rating', 'title', 'description')
    list_display = ('reviewer_display', 'reviewee', 'rating', 'title', 'short_description')
    list_filter = ('reviewer', 'reviewee', 'rating')
    list_per_page = 10
    list_select_related = ('reviewer', 'reviewee',)
    ordering = ('reviewer__username', 'reviewee__username')
    search_fields = ('reviewer__username', 'reviewee__username', 'rating', 'title')

    def get_readonly_fields(self, request, record=None):
        return ('reviewer', 'reviewee',) if record else ()

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
    list_filter = ('favourite_map',)
    list_per_page = 10
    list_select_related = ('user', 'favourite_map',)
    ordering = ('user__username',)
    search_fields = ('user__username', 'favourite_map__map_name', 'score')

    class Media:
        css = {"all": ("css/hide_delete.css",)}

    def get_readonly_fields(self, request, record=None):
        return ('user', 'favourite_map') if record else ()

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    def has_add_permission(self, request):
        return False

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    autocomplete_fields = ('winner', 'loser')
    fields = ('winner', 'loser', 'score_display', 'duration', 'date')
    list_display = ('winner_display', 'loser_display', 'score_display', 'duration', 'date')
    list_filter = ('winner', 'loser')
    list_per_page = 10
    list_select_related = ('winner', 'winner__user', 'loser', 'loser__user')
    ordering = ('date','winner__user__username', 'loser__user__username')
    search_fields = ('winner__user__username','loser__user__username', 'duration','date')

    def save_model(self, request, record, form, change):
        if record.winner: record.winner_name = record.winner.user.username
        if record.loser: record.loser_name = record.loser.user.username
        super().save_model(request, record, form, change)

    def get_readonly_fields(self, request, record=None):
        return ('winner', 'loser', 'duration', 'date') if record else ()

    @admin.display(ordering='winner__user__username', description="Winner")
    def winner_display(self, record):
        return record.winner.user.username if record.winner else f"{record.winner_name} (deleted)"

    @admin.display(ordering='loser__user__username', description="Loser")
    def loser_display(self, record):
        return record.loser.user.username if record.loser else f"{record.loser_name} (deleted)"

@admin.register(MatchStats)
class MatchStatsAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user', 'match')
    fields = ('user', 'kills', 'match', 'deaths', 'points')
    list_display = ('user_display', 'match', 'kills', 'deaths', 'points')
    list_filter = ('user',)
    list_per_page = 10
    list_select_related = ('user', 'user__user', 'match')
    ordering = ('match', 'user__user__username')
    search_fields = ('user__user__username', 'match')

    class Media:
        css = {"all": ("css/hide_delete.css",)}

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    def get_readonly_fields(self, request, record=None):
        return ('user', 'match') if record else ()

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
    list_filter = ('country',)
    list_per_page = 10
    list_select_related = ('counter_user','counter_user__user')
    ordering = ('global_position',)
    readonly_fields = ('country', 'counter_user', 'global_position')
    search_fields = ('counter_user__user__username','country__country_name', 'global_position')

    class Media:
        css = {"all": ("css/hide_delete.css",)}

    @admin.display(ordering='counter_user__score')
    def score(self, record):
        return record.counter_user.score

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    def has_add_permission(self, request):
        return False

@admin.register(LocalRanking)
class LocalRankingAdmin(admin.ModelAdmin):
    autocomplete_fields = ('counter_user',)
    list_display = ('counter_user', 'score', 'country', 'local_position')
    list_filter = ('country',)
    list_per_page = 10
    list_select_related = ('counter_user','counter_user__user')
    ordering = ('country', 'local_position',)
    readonly_fields = ('country', 'counter_user', 'local_position')
    search_fields = ('counter_user__user__username','country__country_name', 'local_position')

    class Media:
        css = {"all": ("css/hide_delete.css",)}

    @admin.display(ordering='counter_user__score')
    def score(self, record):
        return record.counter_user.score

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    def has_add_permission(self, request):
        return False