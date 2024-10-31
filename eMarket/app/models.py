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
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10,default=0)
    stock = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(null=True,auto_now_add=True)
    seller_username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, limit_choices_to={'user_type': 'seller'}, related_name='products')

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'buyer'})
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    items = models.ForeignKey(Cart, on_delete=models.CASCADE)