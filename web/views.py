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

class MyLoginView(LoginView):
    template_name = 'pages/login.html'