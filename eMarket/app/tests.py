from django.test import TestCase, Client
from .models import User, Product, Cart, Order
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.
class testUser(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='adminUser', password='adminPass', user_type='admin')
        User.objects.create_user(username='buyerUser', password='buyerPass', user_type='buyer')
        User.objects.create_user(username='sellerUser', password='sellerPass', user_type='seller')
        User.objects.create_superuser(username='anotherAdmin', password='password123', user_type='admin')

    def test_Admin(self):
        print("\nTest: test_Admin")
        admin = User.objects.get(pk=1)
        self.assertEqual(admin.user_type, 'admin')
        print("User is of admin type.")
        self.assertEqual(admin.pk, 1)
        print("User has the correct id.")

    def test_Buyer(self):
        print("\nTest: test_Buyer")
        buyer = User.objects.get(pk=2)
        self.assertEqual(buyer.user_type, 'buyer')
        print("User is of buyer type.")
        self.assertEqual(buyer.pk, 2)
        print("User has the correct userID.")

    def test_Seller(self):
        print("\nTest: test_Seller")
        seller = User.objects.get(pk=3)
        self.assertEqual(seller.user_type, 'seller')
        print("User is of seller type.")
        self.assertEqual(seller.pk, 3)
        print("User has the correct userID.")

    def test_UserSearching(self):
        print("\nTest: test_UserSearching")
        buyer = User.objects.get(username='buyerUser')
        self.assertEqual(buyer.pk, 2)
        print("Username search works correctly.")
        userCount = User.objects.all().count()
        self.assertEqual(userCount, 4)
        print("Number of users is correct.")
        adminCount = User.objects.filter(user_type='admin').count()
        self.assertEqual(adminCount, 2)
        print("Number of admins is correct.")

class testProduct(TestCase):
    def setUp(self):
        Product.objects.create(name="Phone", price=10)

    def test_ProductExists(self):
        print("\nTest: test_ProductExists")
        phone = Product.objects.get(name="Phone")
        self.assertIsNotNone(phone)
        print("Product found.")
        self.assertEqual(phone.price, 10)
        print("Product price matches.")

#  Test cases for views.py
class testView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='password')

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/product_list.html')

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/login.html')

    def test_login_view_post_valid(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/register.html')

    def test_register_view_post_valid(self):
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
        response = self.client.get(reverse('registration_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/registration_success.html')
