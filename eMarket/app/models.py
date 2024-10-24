from django.db import models
from django.contrib.auth.models import AbstractUser

# holders for now since these models will be redefined after 
# the databases are complete & migrated. just placeholders RN ** do Not make migrations yet**

class User(AbstractUser):

    #accountBalance = models.IntegerField() # Possibly unneeded, as we will not need to have an account balance
    userID = models.PositiveIntegerField(default=-1,primary_key=True) # User ID is non-functional until we can reference the length of the user database
    """"
    user_types = [
        'admin',
        'buyer',
        'seller',
    ]
    user_type = models.CharField(max_length=20, choices=user_types)
    """

class Admin(User):
    user_type = models.CharField(max_length=10,default='admin')


class Buyer(User):
    user_type = models.CharField(max_length=10,default='buyer')


class Seller(User):
    user_type = models.CharField(max_length=10,default='seller')

    

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    
class Cart(models.Model):
    user = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Order(models.Model):
    items = models.ForeignKey(Cart,on_delete=models.CASCADE)