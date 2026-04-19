"""
URL configuration for Strike1v1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from web import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path('play', views.play, name='play'),
    path('tos', views.terms_of_service, name='tos'),
    path('privacy', views.privacy_policy, name='privacy'),
    path('cookies', views.cookie_policy, name='cookies'),
]
