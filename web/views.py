from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import JsonResponse
import requests
from django.conf import settings
from .models import CounterUser, Country, Match, WebUser, Review
from .services import matchmaking
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import update_session_auth_hash, logout
from web.forms import SignUpForm, UserProfileForm, ReviewForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


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
    players = CounterUser.objects.all().order_by('-score')

    if country_iso:
        players = players.filter(user__user_country__country_iso=country_iso)

    people_per_page = 5
    paginator = Paginator(players, people_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    user_page = None
    if request.user.is_authenticated:
        try:
            current_counter_user = request.user.corresponding_CS_user

            player_ids = list(players.values_list('pk', flat=True))

            if current_counter_user.pk in player_ids:
                user_index = player_ids.index(current_counter_user.pk)
                user_page = (user_index // people_per_page) + 1
        except Exception:
            pass

    selected_country = None
    if country_iso:
        selected_country = countries.filter(country_iso=country_iso).first()

    return render(request, 'pages/leaderboard.html', {
        'page_obj': page_obj,
        'countries': countries,
        'selected_country': selected_country,
        'user_page': user_page,
    })


@login_required
def profile_edit(request):
    counter_user = request.user.corresponding_CS_user

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            data = request.POST.copy()
            if 'username' not in data:
                data['username'] = request.user.username
            if 'email' not in data:
                data['email'] = request.user.email

            user_form = UserProfileForm(data, request.FILES, instance=request.user)
            password_form = PasswordChangeForm(request.user)

            if user_form.is_valid():
                user = user_form.save(commit=False)

                if 'delete_image' in request.POST:
                    if user.user_image:
                        user.user_image.delete(save=False)

                user.save()

                selected_map = user_form.cleaned_data.get('favourite_map')
                counter_user.favourite_map = selected_map
                counter_user.save()

                messages.success(request, 'Profile updated successfully.')
                return redirect('web:profile')
            else:
                messages.error(request, 'Error updating profile information.')

        elif 'change_password' in request.POST:
            user_form = UserProfileForm(instance=request.user, initial={'favourite_map': counter_user.favourite_map})
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password updated successfully.')
                return redirect('web:profile')
            else:
                messages.error(request, 'Error updating the password.')
    else:
        user_form = UserProfileForm(instance=request.user, initial={'favourite_map': counter_user.favourite_map})
        password_form = PasswordChangeForm(request.user)

    for field in password_form.fields.values():
        field.widget.attrs.update({
            'class': 'bg-white border-2 border-black px-3 py-2 text-black font-black text-xs focus:outline-none w-full shadow-[inset_2px_2px_0px_rgba(0,0,0,0.2)] mb-3'
        })

    return render(request, 'pages/profile.html', {
        'user_form': user_form,
        'password_form': password_form,
    })


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('web:index')
    return redirect('web:profile')


def reviews(request):
    return render(request, 'pages/reviews.html')


def user_reviews_list(request, username):
    target_user = get_object_or_404(WebUser, username=username)
    my_review = None

    if request.user.is_authenticated:
        my_review = Review.objects.filter(reviewer=request.user, reviewee=target_user).first()

    if request.method == 'POST':
        if not request.user.is_authenticated or request.user == target_user:
            return redirect('login')

        form = ReviewForm(request.POST, instance=my_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewer_name = request.user.username
            review.reviewee = target_user
            review.save()
            return redirect('web:user_reviews_list', username=username)
    else:
        form = ReviewForm(instance=my_review)

    all_other_reviews = Review.objects.filter(reviewee=target_user).order_by('-review_id')
    if request.user.is_authenticated:
        all_other_reviews = all_other_reviews.exclude(reviewer=request.user)

    paginator = Paginator(all_other_reviews, 5)
    page_number = request.GET.get('page')
    other_reviews_page = paginator.get_page(page_number)

    return render(request, 'pages/reviews_list.html', {
        'target_user': target_user,
        'my_review': my_review,
        'form': form,
        'other_reviews': other_reviews_page,
    })


def review_detail(request, username, review_id):
    review = get_object_or_404(Review, review_id=review_id, reviewee__username=username)
    is_author = (review.reviewer == request.user)

    form = None
    if is_author:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('web:review_detail', username=username, review_id=review_id)
        else:
            form = ReviewForm(instance=review)

    return render(request, 'pages/review_detail.html', {
        'review': review,
        'is_author': is_author,
        'form': form
    })


@login_required
def delete_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=review_id)

        target_username = review.reviewee.username

        if review.reviewer == request.user:
            review.delete()
            return redirect('web:user_reviews_list', username=target_username)

    return redirect('web:index')


@login_required
def matches(request):
    counter_user = request.user.corresponding_CS_user

    match_list = Match.objects.filter(
        Q(winner=counter_user) | Q(loser=counter_user)
    ).order_by('-date')

    paginator = Paginator(match_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/matches.html', {
        'page_obj': page_obj,
        'counter_user': counter_user
    })


@login_required
def play(request):
    return render(request, 'pages/play.html')

@login_required
def waiting(request):
    # This view just renders the page, JS will handle the rest
    return render(request, 'pages/waiting.html')

@login_required
def matchmaking_join(request):
    user = request.user
    score = user.corresponding_CS_user.score
    result = matchmaking.join_queue(user.id, score)
    return JsonResponse(result)

@login_required
def matchmaking_status(request):
    user = request.user
    result = matchmaking.get_status(user.id)
    
    # If it was matched, we fetch the real server URL from the controller API
    if result.get("status") == "matched":
        opponent_id = result.get("opponent_id")
        try:
            opponent = WebUser.objects.get(id=opponent_id)
            result["opponent_name"] = opponent.username
            
            # Call the external game server controller
            try:
                # We send the match ID or user IDs to the controller
                # Assuming the controller expects a POST or GET with some info
                api_response = requests.post(
                    settings.GAME_SERVER_API_URL,
                    json={
                        "player1_id": user.id,
                        "player2_id": opponent_id,
                        "matchmaking_timestamp": result.get("timestamp")
                    },
                    timeout=5
                )
                if api_response.status_code == 200:
                    api_data = api_response.json()
                    result["match_url"] = api_data.get("server_url", "Server allocating...")
                else:
                    result["match_url"] = "Error starting server"
            except requests.RequestException:
                result["match_url"] = "Controller offline"

        except WebUser.DoesNotExist:
            result["opponent_name"] = "Unknown"
            result["match_url"] = "#"

    return JsonResponse(result)

@login_required
def matchmaking_cancel(request):
    user = request.user
    matchmaking.cancel_queue(user.id)
    return JsonResponse({"status": "cancelled"})

@login_required
def matchmaking_timeout(request):
    # Called by frontend when they want to widen search
    user = request.user
    matchmaking.increment_attempts(user.id)
    return JsonResponse({"status": "attempts_incremented"})


def terms_of_service(request):
    return render(request, 'legal/tos.html')


def privacy_policy(request):
    return render(request, 'legal/privacy.html')


def cookie_policy(request):
    return render(request, 'legal/cookies.html')
