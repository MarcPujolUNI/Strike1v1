from django.shortcuts import render
from .models import CounterUser, Country
from django.urls import reverse_lazy
from django.views.generic import CreateView
from web.forms import SignUpForm
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from .models import MatchQueue, ActiveMatch

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
    if 'current_match_url' in request.session:
        del request.session['current_match_url']
        request.session.modified = True  # Força a guardar el canvi a la DB de sessions
        # Neteja de cua a la DB
        if request.user.is_authenticated:
            MatchQueue.objects.filter(user=request.user).delete()

    return render(request, 'pages/play.html')

def terms_of_service(request):
    return render(request, 'legal/tos.html')

def privacy_policy(request):
    return render(request, 'legal/privacy.html')

def cookie_policy(request):
    return render(request, 'legal/cookies.html')


# web/views.py
def waiting_view(request):
    user = request.user

    # 1. Comprovar si ja ens han assignat una partida activa
    match = ActiveMatch.objects.filter(
        Q(player1=user) | Q(player2=user),
        is_active=True
    ).first()

    if match:
        return render(request, 'pages/waiting.html', {'match_url': match.server_url})

    # 2. Si no tenim partida, busquem un rival a la cua (que no siguem nosaltres)
    # Busquem el que porti més temps esperant (order_by created_at)
    opponent_entry = MatchQueue.objects.exclude(user=user).order_by('created_at').first()

    if opponent_entry:
        # HEM TROBAT RIVAL!
        opponent = opponent_entry.user

        try:
            # Demanem servidor a la FastAPI (cambiar url)
            response = requests.post('http://172.17.0.1:5000/partida-aleatoria', timeout=10)
            if response.status_code == 200:
                server_url = response.json().get('url')

                # Creem la partida activa per a tots dos
                ActiveMatch.objects.create(
                    player1=user,
                    player2=opponent,
                    server_url=server_url
                )

                # Netegem la cua (el rival ja no ha d'esperar)
                opponent_entry.delete()
                # També ens eliminem a nosaltres si hi erem
                MatchQueue.objects.filter(user=user).delete()

                return render(request, 'pages/waiting.html', {'match_url': server_url})
        except Exception as e:
            print(f"Error connectant amb FastAPI: {e}")

    # 3. Si no hi ha ningú a la cua, ens hi afegim
    MatchQueue.objects.get_or_create(
        user=user,
        defaults={'score': user.corresponding_CS_user.score}
    )

    return render(request, 'pages/waiting.html', {'match_url': None})


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

        # Marcar la partida com tancada
        ActiveMatch.objects.filter(
            Q(player1__username__iexact=winner_name) | Q(player2__username__iexact=winner_name),
            is_active=True
        ).update(is_active=False)

        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)