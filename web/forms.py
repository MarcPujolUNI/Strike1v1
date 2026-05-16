from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Country

WebUser = get_user_model()

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter password'})

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flag_map = {str(c.pk): c.flag_image.url for c in Country.objects.all() if c.flag_image}
        placeholders = {'username':'Choose a username', 'email':'example@gmail.com', 'password1':'Enter your password', 'password2':'Confirm your password'}
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'text-black'})
            if field_name in placeholders:
                field.widget.attrs.update({'placeholder': placeholders[field_name]})
            if field_name == 'user_country':
                field.empty_label = "Select your region"

    class Meta:
        model = WebUser
        fields = ("username", "email", "user_country")