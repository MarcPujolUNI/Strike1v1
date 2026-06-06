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
from web import views, api_views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('play/', views.play, name='play'),
    path('tos/', views.terms_of_service, name='tos'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('cookies/', views.cookie_policy, name='cookies'),
    path('profile/', views.profile_edit, name='profile'),
    path('profile/matches/', views.matches, name='matches'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    path('api/search/', api_views.APIUserSearchList.as_view(), name='user_search_ajax'),
    path('api/countries/', api_views.APICountrySearchList.as_view(), name='country_search_ajax'), # <-- Nueva API
    path('users/', views.users_search, name='users_search'),
    path('users/<str:username>/stats/', views.user_stats, name='user_stats'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('reviews/<str:username>/', views.user_reviews_list, name='user_reviews_list'),
    path('reviews/<str:username>/<int:review_id>/', views.review_detail, name='review_detail'),
    path('save-match', views.save_match, name='save_match'),
]
