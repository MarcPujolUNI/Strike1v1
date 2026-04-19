from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView


def home(request):
    return render(request, 'web/home.html')


class PostListView(ListView):
    model = Post
    template_name = 'web/users.html'
    context_object_name = 'userid'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SignUpView(CreateView):
    form_class = UserCreationForm
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

class MyLoginView(LoginView):
    template_name = 'pages/login.html'