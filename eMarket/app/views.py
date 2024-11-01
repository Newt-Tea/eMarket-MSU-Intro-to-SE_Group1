from django.shortcuts import render, redirect
from .models import Product, Cart, Order, User

#Main Product page
def product_list(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'app/product_list.html', {'products': products})
  
#Product Detail Page
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'app/product_detail.html', {'product': product})
  
#Add to Cart

#Main Login Page
from django.contrib.auth import authenticate, login

def login_view(request):
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
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      user.save()
      # I think there is an error here where the user object is being created twice, so I commented this out
      # Create the UserProfile and associate it with the user
      # user_profile = User.objects.create( 
      #   user = user
      #   user_type=form.cleaned_data.get('role')
      # )
      return redirect('registration_success')  # Redirect to success page
  else:
    form = RegistrationForm()
  
  return render(request, 'app/register.html', {'form': form})

from django.contrib.auth.decorators import login_required
@login_required
##
## This needs to be made functional
##
def add_to_cart(request, product_id):
  cart, created = Cart.objects.get_or_create(user=request.user)
  cart.save()
    
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

# Shopping Cart Page
def shopping_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'app/shopping_cart.html', {'cart_items': cart_items})

# Payment Confirmed Page Possibly unnecessary
def payment_confirmed(request):
    # Logic for confirming payment
    return render(request, 'app/payment_confirmed.html')

# Order History Page
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'app/order_history.html', {'orders': orders})

# Logout View
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return render(request, 'app/login.html')
