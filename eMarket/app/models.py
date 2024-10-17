from django.db import models
from django.contrib.auth.models import AbstractUser

# holders for now since these models will be redefined after 
# the databases are complete & migrated. just placeholders RN ** do Not make migrations yet**

class User(AbstractUser):
    accountBalance = models.IntegerField()
    user_types = [
        'admin',
        'buyer',
        'seller',
    ]

# i will change this functionality, just gotta think about this *strokes chin*
    user_types = models.CharField(max_length=20, choices=user_types)
    class Admin:
        def is_admin(self):
            return self.user_type == models.CharField(choice = 'admin')

    class Buyer:
        def is_buyer(self):
            return self.user_type == models.CharField(choice = 'buyer')

    class Seller:
        def is_seller(self):
            return self.user_type == models.CharField(choice = 'seller')
    

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2)
    
class Cart(models.Model):
    user = models.ForeignKey(User.Buyer)
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField()

class Order(models.Model):
    items = models.ForeignKey(Cart)
