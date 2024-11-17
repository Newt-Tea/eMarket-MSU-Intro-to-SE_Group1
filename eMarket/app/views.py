from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ProductCreationForm, ProductSearchForm, UpdateStockForm
from .utils import search
from django.views.decorators.http import require_POST

# Main Product page
def product_list(request):
    """
    Display the list of products with search and sorting functionality.

    This view handles the display of products, allowing users to search for
    products by name and sort them by relevance, price, or name.

    Args:
        request (HttpRequest): The request object containing GET parameters.

    Returns:
        HttpResponse: The rendered product list page with the search form and products.
    """
    form = ProductSearchForm(request.GET or None)
    products = list(Product.objects.all())  # Convert queryset to list for sorting

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        sort_option = form.cleaned_data.get('sort')

        if search_query:
            search_results = search(search_query.lower(), [product.name.lower() for product in products])
            products = [products[i[0]] for i in search_results] 

        if sort_option == 'rel':
            products = products
        elif sort_option == 'price_asc':
            products.sort(key=lambda product: product.price)
        elif sort_option == 'price_desc':
            products.sort(key=lambda product: -product.price)
        elif sort_option == 'name_asc':
            products.sort(key=lambda product: product.name.lower())
        elif sort_option == 'name_desc':
            products.sort(key=lambda product: product.name.lower(), reverse=True)

    return render(request, 'app/product_list.html', {'form': form, 'products': products})
  
  
# Product Detail Page
def product_detail(request, product_id):
    """
    Display the details of a specific product.

    This view handles the display of a single product's details based on the
    provided product ID.

    Args:
        request (HttpRequest): The request object.
        product_id (int): The ID of the product to display.

    Returns:
        HttpResponse: The rendered product detail page with the product information.
    """
    product = Product.objects.get(id=product_id)
    return render(request, 'app/product_detail.html', {'product': product})
  
# Add to Cart

# Main Login Page
from django.contrib.auth import authenticate, login

def login_view(request):
    """
    Handle user login.

    This view handles the login process for users. It authenticates the user
    based on the provided username and password, and redirects them to the
    appropriate dashboard based on their user type.

    Args:
        request (HttpRequest): The request object containing POST parameters.

    Returns:
        HttpResponse: The rendered login page or a redirect to the appropriate dashboard.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            user_profile = User.objects.get(username=user.username)
            # Redirect based on user type
            if user_profile.user_type == 'admin':
                return redirect('admin_dashboard')
            elif user_profile.user_type == 'seller':
                return redirect('seller_dashboard')
            else:
                return redirect('product_list')
        else:
            return render(request, 'app/login.html', {'error': 'Invalid credentials'})

    return render(request, 'app/login.html')

# Main Registration Page
from .forms import RegistrationForm

def register(request):
    """
    Handle user registration.

    This view handles the registration process for new users. It validates the
    registration form and saves the new user to the database.

    Args:
        request (HttpRequest): The request object containing POST parameters.

    Returns:
        HttpResponse: The rendered registration page or a redirect to the registration success page.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('registration_success')  # Redirect to success page
        else:
            print(form.errors)  # Add this line to print form errors
    else:
        form = RegistrationForm()

    return render(request, 'app/register.html', {'form': form})

######################################
########### CART FUNCTIONS ###########
######################################


# Shopping Cart Page
@login_required
def shopping_cart(request):
  cart, created = Cart.objects.get_or_create(user=request.user)
  cartProducts = cart.cartProducts.all() # type: ignore # cartProducts is a related_name on the Cart model
  total = 0
  for item in cartProducts:
    total = total + item.get_total()
    if item.quantity == 0: item.delete()
  return render(request, 'app/shopping_cart.html', {'cartProducts': cartProducts, 'total' : total})

# Add an item to user's cart
def add_to_cart(request, product_id):
  product = Product.objects.get(id=product_id)
  cart, cart_created = Cart.objects.get_or_create(user=request.user)
  cartProduct, cartProduct_created = CartProduct.objects.get_or_create(cart=cart,product=product)
  if not cartProduct_created: cartProduct.quantity += 1; cartProduct.save() # FIXME: quantity += 1 needs to be changed when multiple-item addition is added
  return redirect('shopping_cart')

# Update the quantity of an item in the cart
@login_required
@require_POST
def update_cart_quantity(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    cartProduct = get_object_or_404(CartProduct, cart=cart, product=product)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cartProduct.quantity = quantity
        cartProduct.save()
    else:
        cartProduct.delete()
    return redirect('shopping_cart')

# Payment on the Checkout page
from .forms import PaymentForm
@login_required
def checkout(request):
  if request.method == 'POST':
    form = PaymentForm(request.POST)
    if form.is_valid():
      return redirect('payment_confirmation')
  else:
    form = PaymentForm()

  # for display of total
    cart = Cart.objects.get(user=request.user)
    cartProducts = cart.cartProducts.all() # type: ignore # cartProducts is a related_name on the Cart model
    total = 0
    for item in cartProducts:
      total = total + item.get_total()
  return render(request, 'app/checkout.html', {'form': form, 'total' : total})

# Save total and create an order    
def cart_checkout(request):
  cart = Cart.objects.get(user=request.user)
  cartProducts = cart.cartProducts.all() # type: ignore # cartProducts is a related_name on the Cart model
  total = 0
  quantity = 0
  deletedProducts = []
  for item in cartProducts:
    product = Product.objects.get(pk=item.product.pk)
    total = total + item.get_total()
    quantity = quantity + item.quantity
    product.stock -= item.quantity
    product.save()
    if product.stock <= 0: deletedProducts.append(product)
  Order.objects.create(
    user = request.user,
    cart = cart, 
    total = total, 
    quantity = quantity,
    status = 'Confirmed' 
  )
  for product in deletedProducts:
    product.delete()
  cart.delete()

# Payment Confirmed Page 
def payment_confirmed(request):
  cart_checkout(request)
  return render(request, 'app/payment_confirmed.html')

############################################
######### END OF CART FUNCTIONS ############
############################################

# Holding Page pending account approval
def registration_success(request):
    return render(request, 'app/registration_success.html')

# Product registration page
from .forms import ProductCreationForm

def add_product(request):
  if request.method == 'POST':
    form = ProductCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      user.save()
      # I think there is an error here where the user object is being created twice, so I commented this out
      # Create the UserProfile and associate it with the user
      # user_profile = User.objects.create( 
      #   user = user
      #   user_type=form.cleaned_data.get('role')
      # )
      return redirect('seller_dashboard')  # Redirect to seller_dashboard
  else:
    form = ProductCreationForm()
  
  return render(request, 'app/add_product.html', {'form': form})

@login_required
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user).distinct()
    orders = Order.objects.filter(cart__cartProducts__product__seller=request.user).distinct()
    return render(request, 'app/seller_dashboard.html', {'products': products, 'orders': orders})
  
@login_required
def update_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        form = UpdateStockForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = UpdateStockForm(instance=product)
    return render(request, 'app/update_stock.html', {'form': form, 'product': product})

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductCreationForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('seller_dashboard')
    else:
        form = ProductCreationForm()
    return render(request, 'app/create_product.html', {'form': form})

@login_required
def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    product.delete()
    return redirect('seller_dashboard')
# Order History Page
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'app/order_history.html', {'orders': orders})
  
# Order Detail Page
@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'app/order_detail.html', {'order': order})

# Order Return Page
@login_required
@require_POST
def order_return(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    for product_id, product_details in order.cart_products.items(): # type: ignore #
        print("Product info: ", product_id, product_details)
        name = product_details['name']
        price = float(product_details['price'])
        quantity = int(product_details['quantity'])
        seller = User.objects.get(username=product_details['seller'])
        productObj, created = Product.objects.get_or_create(pk=product_id)
        if created:
            productObj.name = name
            productObj.price = price
            productObj.stock = quantity
            productObj.seller = seller
        else:
            productObj.stock += int(quantity)
        productObj.save()
    order.status = 'Returned'
    order.save()
    return redirect('order_return_success')

# Order Return Success Page
@login_required
def order_return_success(request):
    return render(request, 'app/order_return.html')

# Logout View
from django.contrib.auth import logout


@require_POST
def logout_view(request):
  logout(request)
  return render(request, 'app/logout.html')


################################
####### ADMIN FUNCTIONS ########
################################

@login_required
def admin_dashboard(request):
  return render(request, 'app/admin_dashboard.html')

# Account management
from django.forms import formset_factory
from .forms import AccountManagementForm
@login_required
def user_list(request):
    users = User.objects.filter(pending=True)
    AccountManagementFormSet = formset_factory(AccountManagementForm, extra=0)
    formset = AccountManagementFormSet(initial=[
        {
            'id': user.id,
            'username': user.username, 
            'user_type': user.user_type, 
            'pending': True
        } for user in users
    ])

    if request.method == 'POST':
        formset = AccountManagementFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                user_id = form.cleaned_data['id']
                user = User.objects.filter(id=user_id).first()
                option = form.cleaned_data['pending']
                if option == 'True':
                    user.delete()
                else:
                    user.pending = False
                    user.save()
            return redirect('user_list')
        if not formset.is_valid():
            print("Formset errors:", formset.errors)
    return render(request, 'app/user_list.html', {'formset': formset, 'users': users})


def home(request):
  return render(request, 'app/home.html')