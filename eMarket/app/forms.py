from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product

# needs a view & page for this one
class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = "__all__"
        role = forms.ChoiceField(choices=User.user_types)

class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("username","password")
