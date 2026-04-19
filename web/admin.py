from django.contrib import admin
from .models import *

@admin.register(WebUser)
class WebUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_country')
    list_filter = ('username', 'user_country')
    search_fields = ('username', 'user_country')

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_id', 'country_name')
    list_filter = ('country_name', )
    search_fields = ('country_name', )