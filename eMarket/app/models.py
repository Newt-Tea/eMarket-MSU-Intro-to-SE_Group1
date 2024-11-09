from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
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
    price = models.DecimalField(decimal_places=2, max_digits=10,default=Decimal(0), validators=[MinValueValidator(0, message='Please enter a valid price.')],)
    stock = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(null=True,auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, limit_choices_to={'user_type': 'seller'}, related_name='products')
    image = models.ImageField(default="default.jpeg", upload_to="media/", blank=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_order_id = models.PositiveIntegerField(default=1)
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True)
    cart_products = models.JSONField(null=True)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0))
    status = models.CharField(max_length = 50, default='Pending')
    date_created = models.DateTimeField(null=True,auto_now_add=True)
    
    def save(self, *args, **kwargs):
        """
        Custom save method to populate `user_order_id` for new orders and the products field from the CartProduct items.
        """
        # Only assign a new user_order_id if this is a new order
        if self._state.adding:
            # Calculate user_order_id based on the user's existing orders
            self.user_order_id = Order.objects.filter(user=self.user).count() + 1

        # Populate cart_products if empty and there's an associated cart
        if not self.cart_products and self.cart:
            self.populate_order_cart_products()

        # Save the order
        super().save(*args, **kwargs)
    
    def populate_order_cart_products(self):
        """
        Builds a dictionary from the CartProduct items in the connected cart.
        Store the product's id and its quantity. Format = { 1:2, 2:1 }, where Product1 has a quantity of 2,
        and Product2 has a quantity of 1.
        """
        cart = self.cart
        if cart:
            cart_products = cart.cartProducts.all()
            products_dict = {
                cart_product.product.pk: {
                    'name': cart_product.product.name,
                    'price': str(cart_product.product.price),
                    'quantity': str(cart_product.quantity),
                    'seller': cart_product.product.seller.username if cart_product.product.seller else None,
                }
                for cart_product in cart_products
            }
            self.cart_products = products_dict
