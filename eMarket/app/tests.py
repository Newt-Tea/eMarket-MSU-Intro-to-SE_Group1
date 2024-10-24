from django.test import TestCase
from .models import User,Admin,Buyer,Seller,Product,Cart,Order

# Create your tests here.
class testUser(TestCase):
    def setUp(self):
        Admin.objects.create_superuser(username='adminUser',email=None,password='pass123')
        Buyer.objects.create_user(username='buyerUser',email=None,password='pass123')
        Seller.objects.create_user(username='sellerUser',email=None,password='pass123',)
        Admin.userID = 0
        Buyer.userID = 1
        Seller.userID = 2
        
    def test_Admin(self):
        print("\nTest: test_Admin")
        admin = Admin.objects.get(userID=0)
        self.assertEqual(admin.user_type,'admin')
        print("User is of admin type.")
        self.assertEqual(admin.userID,0)
        print("User has the correct userID.")
    
    def test_Buyer(self):
        print("\nTest: test_Buyer")
        buyer = Buyer.objects.get(userID=1)
        self.assertEqual(buyer.user_type,'buyer')
        print("User is of buyer type.")
        self.assertEqual(buyer.userID,1)
        print("User has the correct userID.")

    def test_Seller(self):
        print("\nTest: test_Seller")
        seller = Seller.objects.get(userID=2)
        self.assertEqual(seller.user_type,'seller')
        print("User is of seller type.")
        self.assertEqual(seller.userID,2)
        print("User has the correct userID.")
        

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