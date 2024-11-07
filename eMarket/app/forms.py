from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product

class RegistrationForm(UserCreationForm, ModelForm):
    user_type = forms.ChoiceField(widget=forms.Select,choices=User.USER_TYPE_CHOICES)
    class Meta:
        model = User
        fields = ['user_type', 'username', 'password1', 'password2']

class ProductCreationForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','stock','image']
        labels = {
            'name' : 'Item Name',
            'price' : 'Price $',
            'stock' : 'Stock'
            }
        
class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length = 16, label='Card Number')
    expiry_date = forms.CharField(max_length = 5, label='Expiry Date (MM/YY)')
    cvv = forms.CharField(max_length = 3, label='CVV')

class ProductSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search products...'}),
        label=''
    )
    SORT_CHOICES = [
        ('rel','Relevance'),
        ('price_asc', 'Price: Low to High'),
        ('price_desc', 'Price: High to Low'),
        ('name_asc', 'Name: A to Z'),
        ('name_desc', 'Name: Z to A')
    ]
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label=''
    )