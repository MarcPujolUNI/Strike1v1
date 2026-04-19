from django.shortcuts import render
from .models import CounterUser, Country
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
    country_iso = request.GET.get('country')

    countries = Country.objects.all().order_by('country_name')

    players = CounterUser.objects.all()
    if country_iso:
        players = players.filter(user__user_country__country_iso=country_iso)

    selected_country = None
    if country_iso:
        selected_country = Country.objects.filter(country_iso=country_iso).first()

    context = {
        'players': players,
        'countries': countries,
        'selected_country': selected_country,
    }
    return render(request, 'pages/leaderboard.html', context)

def play(request):
    return render(request, 'pages/play.html')

def terms_of_service(request):
    return render(request, 'legal/tos.html')

def privacy_policy(request):
    return render(request, 'legal/privacy.html')

def cookie_policy(request):
    return render(request, 'legal/cookies.html')