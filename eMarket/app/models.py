from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    # To-do: image feature 
    # image = models.ImageField(upload_to='products/')

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'buyer'})
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def get_total(self):
        return self.quantity * self.product.price
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'buyer'})
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length = 50, default='Pending')
