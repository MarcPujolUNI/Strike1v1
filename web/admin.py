from django.contrib import admin
from .models import *

@admin.register(WebUser)
class WebUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_country')
    list_filter = ('username', 'user_country')
    search_fields = ('username', 'user_country')
