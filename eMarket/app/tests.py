from django.test import TestCase, Client
from .models import *
from django.urls import reverse
from django.contrib.auth import get_user_model

# Test cases for user model
class testUser(TestCase):
    def setUp(self):
        # Create test users and assign to self for easier access in tests
        self.adminUser = User.objects.create_superuser(username='adminUser', password='adminPass', user_type='admin')
        self.buyerUser = User.objects.create_user(username='buyerUser', password='buyerPass', user_type='buyer')
        self.sellerUser = User.objects.create_user(username='sellerUser', password='sellerPass', user_type='seller')
        self.anotherAdmin = User.objects.create_superuser(username='anotherAdmin', password='password123', user_type='admin')

    def test_Admin(self):
        print("\nTest: test_Admin")
        # Check that admin user is of correct type and has expected ID
        self.assertEqual(self.adminUser.user_type, 'admin', "User should be of admin type.")
        self.assertEqual(self.adminUser.pk, 1, "Admin user should have primary key 1.")

    def test_Buyer(self):
        print("\nTest: test_Buyer")
        # Check that buyer user is of correct type and has expected ID
        self.assertEqual(self.buyerUser.user_type, 'buyer', "User should be of buyer type.")
        self.assertEqual(self.buyerUser.pk, 2, "Buyer user should have primary key 2.")

    def test_Seller(self):
        print("\nTest: test_Seller")
        # Check that seller user is of correct type and has expected ID
        self.assertEqual(self.sellerUser.user_type, 'seller', "User should be of seller type.")
        self.assertEqual(self.sellerUser.pk, 3, "Seller user should have primary key 3.")

    def test_UserSearching(self):
        print("\nTest: test_UserSearching")
        # Verify username search and count of users
        userCount = User.objects.all().count()
        adminCount = User.objects.filter(user_type='admin').count()

        self.assertEqual(self.buyerUser.pk, 2, "Username search should return the correct user ID.")
        self.assertEqual(userCount, 4, "The total number of users should be 4.")
        self.assertEqual(adminCount, 2, "The number of admin users should be 2.")
        
    def test_UserPassword(self):
        print("\nTest: test_UserPassword")
        # Verify that the passwords are set correctly and can be authenticated
        self.assertTrue(self.adminUser.check_password('adminPass'), "Admin user's password should be 'adminPass'.")
        self.assertTrue(self.buyerUser.check_password('buyerPass'), "Buyer user's password should be 'buyerPass'.")
        self.assertTrue(self.sellerUser.check_password('sellerPass'), "Seller user's password should be 'sellerPass'.")
        self.assertTrue(self.anotherAdmin.check_password('password123'), "Another admin user's password should be 'password123'.")

# Test cases for product model
class testProduct(TestCase):
    def setUp(self):
        # Create test product and assign to self
        self.phone = Product.objects.create(name="Phone", price=10)

    def test_ProductExists(self):
        print("\nTest: test_ProductExists")
        # Verify product exists and check price
        self.assertIsNotNone(self.phone, "Product 'Phone' should exist.")
        self.assertEqual(self.phone.price, 10, "Product price should be 10.")

# Test cases for cart model
class testCart(TestCase):
    def setUp(self):
        # Create test user and cart, assign to self
        self.user = User.objects.create_user(username='buyerUser', password='buyerPass', user_type='buyer')
        self.cart = Cart.objects.create(user=self.user)
        self.sellerUser = User.objects.create_user(username='sellerUser', password='sellerPass', user_type='seller')
    
    def test_CartExists(self):
        print("\nTest: test_CartExists")
        # Verify cart exists for user
        self.assertIsNotNone(self.cart, "Cart for 'buyerUser' should exist.")
        
    def test_cart_deletion(self):
        print("\nTest: test_cart_deletion")
        self.cart.delete()
        self.assertFalse(Cart.objects.filter(user=self.user).exists())


# Test cases for cart product model
class testCartProduct(TestCase):
    def setUp(self):
        # Create test users, carts, products, and assign to self
        self.user1 = User.objects.create_user(username='buyerUser1', password='buyerPass1', user_type='buyer')
        self.user2 = User.objects.create_user(username='buyerUser2', password='buyerPass2', user_type='buyer')
        self.cart1 = Cart.objects.create(user=self.user1)
        self.cart2 = Cart.objects.create(user=self.user2)
        self.product1 = Product.objects.create(name="Phone", price=100.00)
        self.product2 = Product.objects.create(name="Book", price=10.00)

        # Create CartProduct entries
        self.cartProduct1 = CartProduct.objects.create(cart=self.cart1, product=self.product1)
        self.cartProduct2 = CartProduct.objects.create(cart=self.cart1, product=self.product2, quantity=10)
        self.cartProduct3 = CartProduct.objects.create(cart=self.cart2, product=self.product1, quantity=2)
        self.cartProduct4 = CartProduct.objects.create(cart=self.cart2, product=self.product2, quantity=5)
    
    def test_CartProductExists(self):
        print("\nTest: test_CartProductsExists")
        # Verify all CartProducts exist
        self.assertTrue(CartProduct.objects.filter(cart=self.cart1, product=self.product1).exists(), "CartProduct for 'buyerUser1' and 'Phone' should exist.")
        self.assertTrue(CartProduct.objects.filter(cart=self.cart1, product=self.product2).exists(), "CartProduct for 'buyerUser1' and 'Book' should exist.")
        self.assertTrue(CartProduct.objects.filter(cart=self.cart2, product=self.product1).exists(), "CartProduct for 'buyerUser2' and 'Phone' should exist.")
        self.assertTrue(CartProduct.objects.filter(cart=self.cart2, product=self.product2).exists(), "CartProduct for 'buyerUser2' and 'Book' should exist.")
        
    def test_CartProductQuantity(self):
        print("\nTest: test_CartProductQuantity")
        # Verify CartProduct quantities
        self.assertEqual(self.cartProduct1.quantity, 1, "Quantity for CartProduct 'buyerUser1' and 'Phone' should be 1.")
        self.assertEqual(self.cartProduct2.quantity, 10, "Quantity for CartProduct 'buyerUser1' and 'Book' should be 10.")
        self.assertEqual(self.cartProduct3.quantity, 2, "Quantity for CartProduct 'buyerUser2' and 'Phone' should be 2.")
        self.assertEqual(self.cartProduct4.quantity, 5, "Quantity for CartProduct 'buyerUser2' and 'Book' should be 5.")
        
    def test_CartProductDeletion(self):
        print("\nTest: test_CartProductDeletion")
        
        # Delete specific CartProducts
        self.cartProduct1.delete()
        self.cartProduct4.delete()

        # Assert deleted CartProducts no longer exist
        self.assertFalse(CartProduct.objects.filter(cart=self.cart1, product=self.product1).exists(), "CartProduct 'buyerUser1' and 'Phone' should be deleted.")
        self.assertFalse(CartProduct.objects.filter(cart=self.cart2, product=self.product2).exists(), "CartProduct 'buyerUser2' and 'Book' should be deleted.")
        
        # Assert remaining CartProducts still exist
        self.assertTrue(CartProduct.objects.filter(cart=self.cart1, product=self.product2).exists(), "CartProduct 'buyerUser1' and 'Book' should still exist.")
        self.assertTrue(CartProduct.objects.filter(cart=self.cart2, product=self.product1).exists(), "CartProduct 'buyerUser2' and 'Phone' should still exist.")
        
        # Assert that carts and products still exist
        self.assertTrue(Cart.objects.filter(user=self.user1).exists(), "Cart for 'buyerUser1' should still exist.")
        self.assertTrue(Cart.objects.filter(user=self.user2).exists(), "Cart for 'buyerUser2' should still exist.")
        self.assertTrue(Product.objects.filter(name='Phone').exists(), "Product 'Phone' should still exist.")
        self.assertTrue(Product.objects.filter(name='Book').exists(), "Product 'Book' should still exist.")

        
class testOrder(TestCase):
    def setUp(self):
        # Create a user, cart, products, and cart products for testing
        self.user = User.objects.create_user(username='buyerUser', password='buyerPass', user_type='buyer')
        self.cart = Cart.objects.create(user=self.user)
        self.product1 = Product.objects.create(name="Phone", price=500)
        self.product2 = Product.objects.create(name="Book", price=20)
        
        # Create CartProduct entries
        self.cartProduct1 = CartProduct.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.cartProduct2 = CartProduct.objects.create(cart=self.cart, product=self.product2, quantity=1)

    def test_Order_creation_with_cart(self):
        print("\nTest: test_Order_creation_with_cart")
        # Create an order associated with the cart
        order = Order.objects.create(user=self.user, cart=self.cart, total=1020)

        # Check that the order was created and saved
        self.assertIsNotNone(order, "Order should be created successfully.")

        # Verify that cart_products field is populated based on CartProduct items
        expected_cart_products = {
            self.product1.pk: {
                'name': self.product1.name,
                'price': f"{float(self.product1.price):.2f}",
                'quantity': str(self.cartProduct1.quantity),
                'seller': self.product1.seller.username if self.product1.seller else None,
            },
            self.product2.pk: {
                'name': self.product2.name,
                'price': f"{float(self.product2.price):.2f}",
                'quantity': str(self.cartProduct2.quantity),
                'seller': self.product2.seller.username if self.product2.seller else None,
            },
        }
        self.assertEqual(order.cart_products, expected_cart_products, "Order's cart_products field should match the cart's items.")

        # Check the total amount and other default values
        self.assertEqual(order.total, 1020, "Order total should match the provided total.")
        self.assertEqual(order.status, 'Pending', "Order status should be 'Pending' by default.")
        self.assertIsNotNone(order.date_created, "Order date_created should be set.")

    def test_Order_cart_products_population_on_save(self):
        print("\nTest: test_Order_cart_products_population_on_save")
        # Create an order with cart but without explicitly setting cart_products
        order = Order(user=self.user, cart=self.cart)
        order.save()  # This should trigger the custom save method and populate cart_products

        # Verify that cart_products field is populated from CartProduct items in the associated cart
        expected_cart_products = {
            self.product1.pk: {
                'name': self.product1.name,
                'price': f"{float(self.product1.price):.2f}",  # Format to match stored format
                'quantity': str(self.cartProduct1.quantity),
                'seller': self.product1.seller.username if self.product1.seller else None,
            },
            self.product2.pk: {
                'name': self.product2.name,
                'price': f"{float(self.product2.price):.2f}",  # Format to match stored format
                'quantity': str(self.cartProduct2.quantity),
                'seller': self.product2.seller.username if self.product2.seller else None,
            },
        }
        
        self.assertEqual(order.cart_products, expected_cart_products, "Order's cart_products field should auto-populate from CartProduct items.")

    def test_Order_without_cart(self):
        print("\nTest: test_Order_without_cart")
        # Create an order without a cart
        order = Order.objects.create(user=self.user, cart=None, total=100)

        # Ensure cart_products remains None since there's no cart to populate from
        self.assertIsNone(order.cart_products, "Order's cart_products field should be None when no cart is associated.")
        self.assertEqual(order.total, 100, "Order total should match the provided total.")

    

# Test cases for views
class testView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='password')

    def test_product_list_view(self):
        print("\nTest: test_product_list_view")
        # Test product list view status and template
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/product_list.html')

    def test_login_view_get(self):
        print("\nTest: test_login_view_get")
        # Test login view GET request status and template
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/login.html')

    def test_login_view_post_valid(self):
        print("\nTest: test_login_view_post_valid")
        # Test login view POST request with valid credentials
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_register_view_get(self):
        print("\nTest: test_register_view_get")
        # Test register view GET request status and template
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/register.html')

    def test_register_view_post_valid(self):
        print("\nTest: test_register_view_post_valid")
        # Test register view POST request with valid data
        response = self.client.post(reverse('register'), {
            'user_type': 'buyer',
            'username': 'newuser',
            'password1': 'AsUperGreaTPassw0rd!',
            'password2': 'AsUperGreaTPassw0rd!',
        })
        # Verify that the user was created
        user_exists = get_user_model().objects.filter(username='newuser').exists()
        self.assertTrue(user_exists, "New user was not created.")

    def test_registration_success_view(self):
        print("\nTest: test_registration_success_view")
        # Test registration success view status and template
        response = self.client.get(reverse('registration_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/registration_success.html')