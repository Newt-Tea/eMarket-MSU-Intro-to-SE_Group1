from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product

class RegistrationForm(UserCreationForm, ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    user_type = forms.ChoiceField(widget=forms.Select, choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['user_type', 'username', 'password1', 'password2']


class ProductCreationForm(ModelForm):
    """
    A form for creating new products. Includes fields for
    name, price, stock, and image.
    """
    class Meta:
        model = Product
        fields = ['name','price','description','stock','image']

        labels = {
            'name': 'Item Name',
            'price': 'Price $',
            'stock': 'Stock'
        }


class UpdateStockForm(forms.ModelForm):
    """
    A form for updating the stock of a product.
    """
    class Meta:
        model = Product
        fields = ['stock']


class PaymentForm(forms.Form):
    """
    A form for processing payments. Includes fields for
    card number, expiry date, and CVV.
    """
    card_number = forms.CharField(max_length=16, label='Card Number')
    expiry_date = forms.CharField(max_length=5, label='Expiry Date (MM/YY)')
    cvv = forms.CharField(max_length=3, label='CVV')


class ProductSearchForm(forms.Form):
    """
    A form for searching products. Includes a search query
    field and a sort field with various sorting options.
    """
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search products...'}),
        label=''
    )
    SORT_CHOICES = [
        ('rel', 'Relevance'),
        ('price_asc', 'Price: Low to High'),
        ('price_desc', 'Price: High to Low'),
        ('name_asc', 'Name: A to Z'),
        ('name_desc', 'Name: Z to A')
    ]
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False
    )

class AccountManagementForm(ModelForm):
    """
    A form for approving or deleting user accounts.
    """
    pending = forms.ChoiceField(
        choices=[(True, 'Deny'), (False, 'Approve')],
        widget=forms.Select,
        label='Approve this account?',
        required=False
    )
    #non editable widgets
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    username = forms.CharField(required=False)
    user_type = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['id','username', 'user_type','pending']
