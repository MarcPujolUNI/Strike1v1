from django.urls import path
from . import views
from .views import MyLoginView

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', MyLoginView.as_view(), name='login'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path('play', views.play, name='play'),
    path('tos', views.terms_of_service, name='tos'),
    path('privacy', views.privacy_policy, name='privacy'),
    path('cookies', views.cookie_policy, name='cookies'),
]