from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from web.forms import SignUpForm

def home(request):
    return render(request, 'pages/home.html')

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
