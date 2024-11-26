from django.test import TestCase, Client
from .models import *
from django.urls import reverse
from django.contrib.auth import get_user_model
from .utils import *
from django.core.exceptions import ValidationError

# Test cases for user model
class testUser(TestCase):
    def setUp(self):
        # Create test users and assign to self for easier access in tests
        self.adminUser = User.objects.create_superuser(username='adminUser', email='admin@example.com', password='adminPass', user_type='admin')
        self.buyerUser = User.objects.create_user(username='buyerUser', password='buyerPass', user_type='buyer')
        self.sellerUser = User.objects.create_user(username='sellerUser', password='sellerPass', user_type='seller')
        self.anotherAdmin = User.objects.create_superuser(username='anotherAdmin', email='anotheradmin@example.com', password='password123', user_type='admin')

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

class testProduct(TestCase):
    def setUp(self):
        # Create a seller user and a buyer user
        self.sellerUser = get_user_model().objects.create_user(username='sellerUser', password='sellerPass', user_type='seller')
        self.buyerUser = get_user_model().objects.create_user(username='buyerUser', password='buyerPass', user_type='buyer')

    def test_ProductExists(self):
        print("\nTest: test_ProductExists")
        # Seller creates a product
        product = Product.objects.create(name="Phone", price=10, seller=self.sellerUser)
        
        # Verify product exists and is associated with the seller
        self.assertIsNotNone(product, "Product 'Phone' should be created by seller.")
        self.assertEqual(product.seller, self.sellerUser, "Product should be associated with 'sellerUser'.")
        self.assertEqual(product.price, 10, "Product price should be 10.")

    def test_ProductStock(self):
        print("\nTest: test_ProductStock")
        # Create a product and check initial stock
        product = Product.objects.create(name="Book", price=20, stock=5, seller=self.sellerUser)
        self.assertEqual(product.stock, 5, "Product 'Book' should have stock of 5.")

    def test_seller_can_create_product(self):
        print("\nTest: test_seller_can_create_product")
        # Seller creates a product
        product = Product.objects.create(name="Laptop", price=1000.00, stock=10, seller=self.sellerUser)
        
        # Verify that the product was created and associated with the seller
        self.assertIsNotNone(product, "Product should be created by seller.")
        self.assertEqual(product.seller, self.sellerUser, "Product should be associated with 'sellerUser'.")
        self.assertEqual(product.name, "Laptop", "Product name should be 'Laptop'.")
        self.assertEqual(product.price, 1000.00, "Product price should be 1000.00.")

    def test_buyer_cannot_create_product(self):
        print("\nTest: test_buyer_cannot_create_product")
        # Attempt to create a product with a buyer user
        with self.assertRaises(ValidationError, msg="Only sellers should be able to create products."):
            Product.objects.create(name="Tablet", price=500.00, stock=5, seller=self.buyerUser)
        
    def test_ProductDeletion(self):
        print("\nTest: test_ProductDeletion")
        # Seller creates and then deletes a product
        product = Product.objects.create(name="Phone", price=10, seller=self.sellerUser)
        product.delete()
        self.assertFalse(Product.objects.filter(name="Phone").exists(), "Product 'Phone' should be deleted.")
        
class testProductSearchSort(TestCase):
    def setUp(self):
        # Create a seller user and several products
        self.sellerUser = get_user_model().objects.create_user(username='sellerUser', password='sellerPass', user_type='seller')
        
        # Create products with different names and prices
        self.product1 = Product.objects.create(name="Phone", price=500, seller=self.sellerUser)
        self.product2 = Product.objects.create(name="Book", price=20, seller=self.sellerUser)
        self.product3 = Product.objects.create(name="Laptop", price=1000, seller=self.sellerUser)
        self.product4 = Product.objects.create(name="Tablet", price=200, seller=self.sellerUser)

    def test_search_product_by_name_lcs(self):
        print("\nTest: test_search_product_by_name_lcs")
        # Use the search function to find products that match "Phone"
        product_names = [p.name for p in Product.objects.all()]
        search_results = search("Phone", product_names)
        
        # Verify that the correct product is found by checking the first item in the sorted search results
        matched_product_index = search_results[0][0] if search_results else None
        self.assertIsNotNone(matched_product_index, "Search should find at least one matching product.")
        self.assertEqual(product_names[matched_product_index].lower(), "phone", "Search should return 'Phone' as the most similar match.") # type: ignore

    def test_search_no_results_lcs(self):
        print("\nTest: test_search_no_results_lcs")
        # Use the search function to find a non-existent product
        product_names = [p.name for p in Product.objects.all()]
        search_results = search("Camera", product_names)
        # Verify that no products are found
        self.assertEqual(len(search_results), 0, "Search should return no results for 'Camera'.")

    def test_sort_products_by_price_ascending(self):
        print("\nTest: test_sort_products_by_price_ascending")
        # Retrieve products and sort by price in ascending order
        products = list(Product.objects.all())
        prices = [product.price for product in products]
        sort(prices)  # Sort prices in ascending order
        
        # Verify that prices are sorted in ascending order
        self.assertEqual(prices, sorted(prices), "Prices should be sorted in ascending order.")

    def test_sort_products_by_price_descending(self):
        print("\nTest: test_sort_products_by_price_descending")
        # Retrieve products and sort by price in descending order
        products = list(Product.objects.all())
        prices = [product.price for product in products]
        sort(prices)
        prices.reverse()  # Reverse to simulate descending order
        
        # Verify that prices are sorted in descending order
        self.assertEqual(prices, sorted(prices, reverse=True), "Prices should be sorted in descending order.")

    def test_search_multiple_matches_lcs(self):
        print("\nTest: test_search_multiple_matches_lcs")
        # Use the search function to find products that partially match "Tab"
        product_names = [p.name for p in Product.objects.all()]
        search_results = search("Tab", product_names)
        
        # Verify that "Tablet" is the most similar match and appears in the search results
        matched_product_index = search_results[0][0] if search_results else None
        self.assertIsNotNone(matched_product_index, "Search should find at least one matching product.")
        self.assertEqual(product_names[matched_product_index].lower(), "tablet", "Search should return 'Tablet' as the most similar match.") # type: ignore

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
        self.assertFalse(Cart.objects.filter(user=self.user).exists(), "Cart for 'buyerUser' should be deleted.")

    def test_CartUserAssociation(self):
        print("\nTest: test_CartUserAssociation")
        # Verify the cart is associated with the correct user
        self.assertEqual(self.cart.user, self.user, "Cart should be associated with 'buyerUser'.")
        self.assertNotEqual(self.cart.user, self.sellerUser, "Cart should not be associated with 'sellerUser'.")

    def test_CartCreationNewUser(self):
        print("\nTest: test_CartCreationNewUser")
        # Create a new user and cart, then verify it exists
        new_user = User.objects.create_user(username='newUser', password='newPass', user_type='buyer')
        new_cart = Cart.objects.create(user=new_user)
        self.assertIsNotNone(new_cart, "Cart for 'newUser' should exist.")
        self.assertEqual(new_cart.user, new_user, "New cart should be associated with 'newUser'.")


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
        print("\nTest: test_CartProductExists")
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

    def test_AddProductToCart(self):
        print("\nTest: test_AddProductToCart")
        # Add a new product to a cart
        new_product = Product.objects.create(name="Tablet", price=300.00)
        cart_product = CartProduct.objects.create(cart=self.cart1, product=new_product, quantity=3)
        
        # Verify the product was added with the correct quantity
        self.assertEqual(cart_product.product, new_product, "New product 'Tablet' should be added to the cart.")
        self.assertEqual(cart_product.quantity, 3, "Quantity for new product 'Tablet' should be 3.")
        self.assertTrue(CartProduct.objects.filter(cart=self.cart1, product=new_product).exists(), "CartProduct for 'buyerUser1' and 'Tablet' should exist.")

    def test_UpdateProductQuantityInCart(self):
        print("\nTest: test_UpdateProductQuantityInCart")
        # Update the quantity of an existing product in the cart
        self.cartProduct2.quantity = 15
        self.cartProduct2.save()
        
        # Verify the quantity has been updated
        self.assertEqual(self.cartProduct2.quantity, 15, "Quantity for CartProduct 'buyerUser1' and 'Book' should be updated to 15.")

        
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

# Test cases for returns
class TestOrderReturn(TestCase):
    def setUp(self):
        # Set up a user, products, cart, and an order with cart products
        self.user = User.objects.create_user(username='testuser', password='password',user_type='seller')
        self.client.login(username='testuser', password='password')
        self.product1 = Product.objects.create(name="Phone", price=500, stock=10, seller=self.user)
        self.product2 = Product.objects.create(name="Book", price=20, stock=5, seller=self.user)
        self.cart = Cart.objects.create(user=self.user)
        self.cartProduct1 = CartProduct.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.cartProduct2 = CartProduct.objects.create(cart=self.cart, product=self.product2, quantity=1)
        self.order = Order.objects.create(
            user=self.user,
            cart=self.cart,
            total=1020,
            cart_products={
                self.product1.pk: {
                    "name": self.product1.name,
                    "price": "500.00",
                    "quantity": "2",
                    "seller": self.user.username,
                },
                self.product2.pk: {
                    "name": self.product2.name,
                    "price": "20.00",
                    "quantity": "1",
                    "seller": self.user.username,
                },
            },
            status='Confirmed'
        )

    def test_return_order_status(self):
        print("\nTest: test_return_order_status")
        # Verify that returning an order updates the status to 'Returned'
        response = self.client.post(reverse('order_return', args=[self.order.pk]))
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Returned', "Order status should be 'Returned' after return.")

    def test_return_order_stock(self):
        print("\nTest: test_return_order_stock")
        # Check that returning an order updates product stock correctly
        original_stock1 = self.product1.stock
        original_stock2 = self.product2.stock
        self.client.post(reverse('order_return', args=[self.order.pk]))
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock, original_stock1 + 2, "Product1 stock should increase by order quantity.")
        self.assertEqual(self.product2.stock, original_stock2 + 1, "Product2 stock should increase by order quantity.")

    def test_return_redirect(self):
        print("\nTest: test_return_redirect")
        # Confirm redirection to success page after returning an order
        response = self.client.post(reverse('order_return', args=[self.order.pk])) # type: ignore
        self.assertRedirects(response, reverse('order_return_success'), msg_prefix="Returning an order should redirect to success page.")

    def test_order_in_history(self):
        print("\nTest: test_order_in_history")
        # Verify that a returned order appears correctly in order history
        self.client.post(reverse('order_return', args=[self.order.pk])) # type: ignore
        response = self.client.get(reverse('order_history'))
        self.assertContains(response, 'Returned', msg_prefix="Returned order should appear with updated status in history.")

    def test_order_detail_after_return(self):
        print("\nTest: test_order_detail_after_return")
        # Check that order detail page displays correctly after return
        self.client.post(reverse('order_return', args=[self.order.pk])) # type: ignore
        response = self.client.get(reverse('order_detail', args=[self.order.pk])) # type: ignore
        self.assertContains(response, 'Returned', msg_prefix="Order detail should display updated status as 'Returned'.")
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

class TestAdminFunctionality(TestCase):
    def setUp(self):
        # Create test users and a seller
        self.adminUser = User.objects.create_superuser(username='admin', password='adminPass', user_type='admin')
        self.buyerUser = User.objects.create_user(username='buyer', password='buyerPass', user_type='buyer', pending=True)
        self.sellerUser = User.objects.create_user(username='seller', password='sellerPass', user_type='seller', pending=True)
        
        # Create products for approval
        self.pendingProduct = Product.objects.create(name="Phone", price=500, seller=self.sellerUser, pending=True)
        self.anotherPendingProduct = Product.objects.create(name="Laptop", price=1000, seller=self.sellerUser, pending=True)

    def test_approve_user(self):
        print("\nTest: test_approve_user")
        # Log in as admin
        self.client.login(username='admin', password='adminPass')
        
        # Simulate approving a user via POST
        response = self.client.post(reverse('user_list'), data={
            'form-0-id': self.buyerUser.id,
            'form-0-pending': 'False',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
        })
        self.assertEqual(response.status_code, 302, "Response should redirect after approval.")
        
        # Verify user is no longer pending
        self.buyerUser.refresh_from_db()
        self.assertFalse(self.buyerUser.pending, "Buyer user should be approved (pending=False).")

    def test_deny_user(self):
        print("\nTest: test_deny_user")
        # Log in as admin
        self.client.login(username='admin', password='adminPass')
        
        # Simulate denying a user via POST
        response = self.client.post(reverse('user_list'), data={
            'form-0-id': self.sellerUser.id,
            'form-0-pending': 'True',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
        })
        self.assertEqual(response.status_code, 302, "Response should redirect after denial.")
        
        # Verify user is deleted
        self.assertFalse(get_user_model().objects.filter(id=self.sellerUser.id).exists(), "Seller user should be deleted.")

    def test_approve_product(self):
        print("\nTest: test_approve_product")
        # Log in as admin
        self.client.login(username='admin', password='adminPass')
        
        # Simulate approving a product via POST
        response = self.client.post(reverse('admin_product_list'), data={
            'form-0-id': self.pendingProduct.id,
            'form-0-pending': 'False',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
        })
        self.assertEqual(response.status_code, 302, "Response should redirect after approval.")
        
        # Verify product is no longer pending
        self.pendingProduct.refresh_from_db()
        self.assertFalse(self.pendingProduct.pending, "Product should be approved (pending=False).")

    def test_deny_product(self):
        print("\nTest: test_deny_product")
        # Log in as admin
        self.client.login(username='admin', password='adminPass')
        
        # Simulate denying a product via POST
        response = self.client.post(reverse('admin_product_list'), data={
            'form-0-id': self.anotherPendingProduct.id,
            'form-0-pending': 'True',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
        })
        self.assertEqual(response.status_code, 302, "Response should redirect after denial.")
        
        # Verify product is deleted
        self.assertFalse(Product.objects.filter(id=self.anotherPendingProduct.id).exists(), "Product should be deleted.")

    def test_verify_approved_product_has_correct_seller(self):
        print("\nTest: test_verify_approved_product_has_correct_seller")
        # Log in as admin
        self.client.login(username='admin', password='adminPass')
        
        # Simulate approving a product via POST
        response = self.client.post(reverse('admin_product_list'), data={
            'form-0-id': self.pendingProduct.id,
            'form-0-pending': 'False',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
        })
        self.assertEqual(response.status_code, 302, "Response should redirect after approval.")
        
        # Verify the product is approved and associated with the correct seller
        self.pendingProduct.refresh_from_db()
        self.assertEqual(self.pendingProduct.seller.username, self.sellerUser.username, "Product should have the correct seller.")
        self.assertFalse(self.pendingProduct.pending, "Product should be approved (pending=False).")

class TestBuyerFunctionality(TestCase):
    def setUp(self):
        # Set up a buyer user and log in
        self.client = Client()
        self.buyerUser = User.objects.create_user(username='buyerUser', password='buyerPass', user_type='buyer')
        self.client.login(username='buyerUser', password='buyerPass')
        self.sellerUser = User.objects.create_user(username='testuser', password='password',user_type='seller')
        self.product = Product.objects.create(name="Book", price=20, stock=5, seller=self.sellerUser)

    def test_buyer_registration(self):
        print("\nTest: test_buyer_registration")
        # Test buyer registration
        response = self.client.post(reverse('register'), {
            'user_type': 'buyer',
            'username': 'newBuyer',
            'password1': 'BuyerPass123!',
            'password2': 'BuyerPass123!',
        })
        user_exists = get_user_model().objects.filter(username='newBuyer').exists()
        print("Input: username='newBuyer', password='BuyerPass123!'")
        print(f"Output: user_exists={user_exists}")
        self.assertTrue(user_exists, "New buyer was not created.")

    def test_buyer_login(self):
        print("\nTest: test_buyer_login")
        # Test buyer login
        response = self.client.post(reverse('login'), {'username': 'buyerUser', 'password': 'buyerPass'})
        print("Input: username='buyerUser', password='buyerPass'")
        print(f"Output: response.status_code={response.status_code}")
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_buyer_view_products(self):
        print("\nTest: test_buyer_view_products")
        # Test viewing products
        response = self.client.get(reverse('product_list'))
        print("Input: GET request to 'product_list'")
        print(f"Output: response.status_code={response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/product_list.html')

    def test_buyer_add_to_cart(self):
        print("\nTest: test_buyer_add_to_cart")
        # Test adding a product to the cart
        product = Product.objects.get(name="Book")
        response = self.client.post(reverse('add_to_cart', args=[product.pk]), {'quantity': 2}) # type: ignore
        cart_product_exists = CartProduct.objects.filter(cart__user=self.buyerUser, product=product).exists()
        print(f"Input: product_id={product.pk}, quantity=2") # type: ignore
        print(f"Output: cart_product_exists={cart_product_exists}")
        self.assertTrue(cart_product_exists, "Product was not added to the cart.")

    def test_buyer_checkout(self):
        print("\nTest: test_buyer_checkout")
        # Test checkout process
        product = Product.objects.get(name="Book")
        cart = Cart.objects.create(user=self.buyerUser)
        CartProduct.objects.create(cart=cart, product=product, quantity=1)
        response = self.client.post(reverse('checkout'), {"card_number": '1234123412341234', "expiry_date": '12/23', "cvv": '123'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_buyer_order_history(self):
        # Test viewing order history
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/order_history.html')

class TestSellerFunctionality(TestCase):
    def setUp(self):
        # Set up a seller user and log in
        self.client = Client()
        self.sellerUser = User.objects.create_user(username='sellerUser', password='sellerPass', user_type='seller')
        self.client.login(username='sellerUser', password='sellerPass')

    def test_seller_create_product(self):
        # Test seller creating a product
        response = self.client.post(reverse('create_product'), {
            'name': 'NewProduct',
            'price': 100.00,
            'description': 'A new product',
            'stock': 10,
            'image': 'image.jpg'
        })
        product_exists = Product.objects.filter(name='NewProduct').exists()
        self.assertTrue(product_exists, "Product was not created by the seller.")

    def test_seller_update_stock(self):
        # Test seller updating product stock
        product = Product.objects.create(name="ExistingProduct", price=50.00, stock=5, seller=self.sellerUser)
        response = self.client.post(reverse('update_stock', args=[product.pk]), {'stock': 20})
        product.refresh_from_db()
        self.assertEqual(product.stock, 20, "Product stock was not updated correctly.")

    def test_seller_remove_product(self):
        # Test seller removing a product
        product = Product.objects.create(name="ProductToRemove", price=30.00, stock=5, seller=self.sellerUser)
        response = self.client.post(reverse('remove_product', args=[product.pk]))
        product_exists = Product.objects.filter(name='ProductToRemove').exists()
        self.assertFalse(product_exists, "Product was not removed by the seller.")

    def test_seller_view_orders(self):
        # Test seller viewing their orders
        response = self.client.get(reverse('seller_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/seller_dashboard.html')

    def test_seller_order_detail(self):
        # Test seller viewing order details
        product = Product.objects.create(name="ProductInOrder", price=100.00, stock=5, seller=self.sellerUser)
        cart = Cart.objects.create(user=self.sellerUser)
        cart_product = CartProduct.objects.create(cart=cart, product=product, quantity=2)
        order = Order.objects.create(user=self.sellerUser, cart=cart, total=200.00)
        response = self.client.get(reverse('order_detail', args=[order.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/order_detail.html')

class TestUserDeletionSystem(TestCase):
    def setUp(self):
        # Create an admin user
        self.adminUser = get_user_model().objects.create_superuser(
            username='admin', password='adminPass', user_type='admin'
        )
        # Create non-admin users
        self.user1 = get_user_model().objects.create_user(
            username='user1', password='user1Pass', user_type='buyer'
        )
        self.user2 = get_user_model().objects.create_user(
            username='user2', password='user2Pass', user_type='seller'
        )
        # Log in as admin
        self.client.login(username='admin', password='adminPass')

    def test_list_non_admin_users(self):
        print("\nTest: test_list_non_admin_users")
        # Access the user deletion page
        response = self.client.get(reverse('user_deletion'))
        self.assertEqual(response.status_code, 200, "Admin should access the user deletion page.")
        # Verify that the non-admin users are listed
        self.assertContains(response, self.user1.username, msg_prefix="User1 should be listed.")
        self.assertContains(response, self.user2.username, msg_prefix="User2 should be listed.")
        self.assertNotContains(response, self.adminUser.username, msg_prefix="Admin should not be listed.")

    def test_delete_user_confirmation_page(self):
        print("\nTest: test_delete_user_confirmation_page")
        # Access the confirmation page for user1
        response = self.client.get(reverse('user_deletion_confirmation', args=[self.user1.id]))
        self.assertEqual(response.status_code, 200, "Admin should access the confirmation page for a user.")
        self.assertContains(response, f"Are you sure you want to delete user \"{self.user1.username}\"?",
                            msg_prefix="The confirmation page should display the correct user.")

    def test_confirm_delete_user(self):
        print("\nTest: test_confirm_delete_user")
        # Confirm deletion of user1
        response = self.client.post(reverse('user_deletion_confirmation', args=[self.user1.id]), data={'yes': True})
        self.assertEqual(response.status_code, 302, "After confirming deletion, admin should be redirected.")
        # Verify that user1 is deleted
        self.assertFalse(get_user_model().objects.filter(id=self.user1.id).exists(), "User1 should be deleted.")

    def test_cancel_delete_user(self):
        print("\nTest: test_cancel_delete_user")
        # Cancel deletion of user2
        response = self.client.post(reverse('user_deletion_confirmation', args=[self.user2.id]), data={'no': True})
        self.assertEqual(response.status_code, 302, "After cancelling deletion, admin should be redirected.")
        # Verify that user2 is not deleted
        self.assertTrue(get_user_model().objects.filter(id=self.user2.id).exists(), "User2 should not be deleted.")

    def test_admin_can_access_user_deletion(self):
        print("\nTest: test_admin_can_access_user_deletion")
        # Log in as admin
        self.client.login(username='admin', password='adminPass')
        response = self.client.get(reverse('user_deletion'))
        self.assertEqual(response.status_code, 200, "Admin should access the user deletion page.")
        self.assertContains(response, "Manage Users", msg_prefix="The page should display 'Manage Users'.")