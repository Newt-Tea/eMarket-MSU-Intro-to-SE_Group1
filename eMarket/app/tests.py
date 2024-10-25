from django.test import TestCase
from .models import User,Product,Cart,Order

# Create your tests here.
class testUser(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='adminUser',email=None,password='adminPass',user_type='admin')
        User.objects.create_user(username='buyerUser',email=None,password='buyerPass',user_type='buyer')
        User.objects.create_user(username='sellerUser',email=None,password='sellerPass',user_type='seller')
        User.objects.create_superuser(username='anotherAdmin',email=None,password='password123',user_type='admin')
    

    def test_Admin(self):
        print("\nTest: test_Admin")
        admin = User.objects.get(pk=1)
        self.assertEqual(admin.user_type,'admin')
        print("User is of admin type.")
        self.assertEqual(admin.pk,1)
        print("User has the correct id.")
        
    def test_Buyer(self):
        print("\nTest: test_Buyer")
        buyer = User.objects.get(pk=2)
        self.assertEqual(buyer.user_type,'buyer')
        print("User is of buyer type.")
        self.assertEqual(buyer.pk,2)
        print("User has the correct userID.")

    def test_Seller(self):
        print("\nTest: test_Seller")
        seller = User.objects.get(pk=3)
        self.assertEqual(seller.user_type,'seller')
        print("User is of seller type.")
        self.assertEqual(seller.pk,3)
        print("User has the correct userID.")
    
    def test_UserSearching(self):
        print("\nTest: test_UserSearching")
        buyer = User.objects.get(username='buyerUser')
        self.assertEqual(buyer.pk,2)
        print("Username search works correctly.")
        userCount = User.objects.all().count()
        self.assertEqual(userCount,4)
        print("Number of users is correct.")
        adminCount = User.objects.filter(user_type='admin').count()
        self.assertEqual(adminCount,2)
        print("Number of admins is correct.")
        
        
        
        

class testProduct(TestCase):
    def setUp(self):
        Product.objects.create(name="Phone",price=10)
        
    def test_ProductExists(self):
        print("\nTest: test_ProductExists")
        phone = Product.objects.get(name="Phone")
        self.assertIsNotNone(phone)
        print("Product found.")
        self.assertEqual(phone.price,10)
        print("Product price matches.")