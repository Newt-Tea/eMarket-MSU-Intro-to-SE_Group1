from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

user_types = [
    ('admin','ADMIN',),
    ('buyer', 'BUYER',),
    ('seller', 'SELLER'),
]

#Needs a password and user type variable
class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(widget=forms.Select,choices=user_types)
    class Meta:
        model = User
        fields = ['role', 'username', 'password1', 'password2']