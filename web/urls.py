from django.urls import path
from . import views
from .views import MyLoginView

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', MyLoginView.as_view(), name='login'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
]