from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CounterUser, Country
from django.urls import reverse_lazy
from django.views.generic import CreateView
from web.forms import SignUpForm, UserProfileForm
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


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

    selected_country = None
    if country_iso:
        selected_country = Country.objects.filter(country_iso=country_iso).first()

    context = {
        'players': players,
        'countries': countries,
        'selected_country': selected_country,
    }
    return render(request, 'pages/leaderboard.html', context)


@login_required
def profile_edit(request):
    counter_user = CounterUser.objects.get(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            user_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
            password_form = PasswordChangeForm(request.user)

            if user_form.is_valid():
                user_form.save()

                selected_map = user_form.cleaned_data.get('favourite_map')
                counter_user.favourite_map = selected_map
                counter_user.save()

                messages.success(request, 'Profile updated successfully.')
                return redirect('web:profile')
            else:
                messages.error(request, 'Error updating profile information.')

        elif 'change_password' in request.POST:
            user_form = UserProfileForm(instance=request.user)
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password updated successfully.')
                return redirect('web:profile')
    else:
        user_form = UserProfileForm(
            instance=request.user,
            initial={'favourite_map': counter_user.favourite_map}
        )
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

@login_required
def reviews(request):
    return render(request, 'pages/reviews.html')

@login_required
def matches(request):
    return render(request, 'pages/matches.html')

def play(request):
    return render(request, 'pages/play.html')


def terms_of_service(request):
    return render(request, 'legal/tos.html')


def privacy_policy(request):
    return render(request, 'legal/privacy.html')


def cookie_policy(request):
    return render(request, 'legal/cookies.html')
