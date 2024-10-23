from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    #accountBalance = models.IntegerField() # Possibly unneeded, as we will not need to have an account balance
    userID = -1 # User ID is non-functional until we can reference the length of the user database
    
    #using this for the sake of the usercreationform
    user_types = [
        ('admin','ADMIN',),
        ('buyer', 'BUYER',),
        ('seller', 'SELLER'),
    ]

    user_type = models.CharField(max_length=20, choices=user_types, default='buyer')
   
class Admin(User):
    user_type = 'admin'
    def is_admin(self):
        return self.user_type == models.CharField(choice = 'admin')

class Buyer(User):
    user_type = 'buyer'
    def is_buyer(self):
        return self.user_type == models.CharField(choice = 'buyer')

class Seller(User):
    user_type = 'seller'
    def is_seller(self):
        return self.user_type == models.CharField(choice = 'seller')
    

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    
class Cart(models.Model):
    user = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Order(models.Model):
    items = models.ForeignKey(Cart,on_delete=models.CASCADE)