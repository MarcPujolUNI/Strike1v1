from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Country, Review
from django import forms

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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = WebUser
        fields = ['username', 'email', 'user_image']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'bg-white border-2 border-black px-3 py-2 text-black font-black text-xs focus:outline-none w-full shadow-[inset_2px_2px_0px_rgba(0,0,0,0.2)]'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'bg-white border-2 border-black px-3 py-2 text-black font-black text-xs focus:outline-none w-full shadow-[inset_2px_2px_0px_rgba(0,0,0,0.2)]'
            }),
            'user_image': forms.FileInput(attrs={
                'class': 'hidden',
                'id': 'avatar-upload',
                'accept': 'image/*'
            })
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'rating', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-black border-2 border-white/10 p-3 text-white font-bold text-xs focus:border-brand-red outline-none transition-all uppercase',
                'placeholder': 'REVIEW TITLE...'
            }),
            'rating': forms.NumberInput(attrs={
                'id': 'rating-value',
                'class': 'hidden',
                'min': '1',
                'max': '5'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full bg-black border-2 border-white/10 p-3 text-white font-bold text-xs focus:border-brand-red outline-none transition-all h-24 resize-none',
                'placeholder': 'PROVIDE A DESCRIPTION OF YOUR EXPERIENCE WITH THE PLAYER...'
            }),
        }