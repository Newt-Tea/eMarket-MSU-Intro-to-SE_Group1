from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product

class RegistrationForm(UserCreationForm, ModelForm):
    role = forms.ChoiceField(widget=forms.Select,choices=User.USER_TYPE_CHOICES)
    class Meta:
        model = User
        fields = ['role', 'username', 'password1', 'password2']

class ProductCreationForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','price']
        labels = {
            'name' : 'Item Name',
            'price' : 'Price $'}