from django.shortcuts import render
from .models import CounterUser, Country
from django.urls import reverse_lazy
from django.views.generic import CreateView
from web.forms import SignUpForm
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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


# web/views.py
def waiting_view(request):
    match_url = request.session.get('current_match_url')

    if not match_url:
        try:
            # CANVIA ip per 172.17.0.1 quan estigui dins del server, sha de probar
            response = requests.post('http://192.168.1.114:5000/partida-aleatoria', timeout=10)

            if response.status_code == 200:
                data = response.json()
                match_url = data.get('url')
                request.session['current_match_url'] = match_url
            else:
                print(f"Error API: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error de connexió amb el Controller: {e}")
            match_url = None

    return render(request, 'pages/waiting.html', {'match_url': match_url})


@csrf_exempt  # Perquè la FastAPI pugui fer POST sense token CSRF
def save_match_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(f"Dades partida Rebudes: {data}")
        # Actualitzar estadístiques
        winner_name = data.get('winner').strip()
        if winner_name and winner_name != "None (Incomplete)":
            # nom del log ha de coincicidir amb l'usuari de Django
            user_profile = CounterUser.objects.filter(user__username__iexact=winner_name).first()
            if user_profile:
                user_profile.score += 25  # Exemple de pujada de punts
                user_profile.save()

        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)