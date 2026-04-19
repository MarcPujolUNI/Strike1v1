from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

WebUser = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = WebUser
        fields = ("username",)