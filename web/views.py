from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from web.forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

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