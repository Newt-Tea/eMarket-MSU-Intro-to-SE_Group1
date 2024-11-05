from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    pending = models.BooleanField(default=True)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10,default=0)
    stock = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(null=True,auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, limit_choices_to={'user_type': 'seller'}, related_name='products')

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'buyer'})

# Through model that defines the relationship between the Product and the Cart
class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # connects to ONE product
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartProducts') # connects to ONE cart
    quantity = models.PositiveIntegerField(default=1) # describes the quantity of the connected product
    def get_total(self): # gets total prices of connected product
        return self.quantity * self.product.price

class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'buyer'})
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length = 50, default='Pending')
