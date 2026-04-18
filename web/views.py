from django.shortcuts import render
from django.contrib.auth.views import LoginView

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, 'pages/dashboard.html')
    else:
        return render(request, 'pages/landing.html')

def leaderboard(request):
    return render(request, 'pages/leaderboard.html')

def play(request):
    return render(request, 'pages/play.html')

def terms_of_service(request):
    return render(request, 'legal/tos.html')

def privacy_policy(request):
    return render(request, 'legal/privacy.html')

def cookie_policy(request):
    return render(request, 'legal/cookies.html')

class MyLoginView(LoginView):
    template_name = 'pages/login.html'