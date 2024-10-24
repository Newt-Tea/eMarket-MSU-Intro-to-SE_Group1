from django.shortcuts import render
from .models import Product, Cart, Order

#Main Product page
def product_list(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'your_app/product_list.html', {'products': products})

#Main Login Page
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .models import User 

def login_view(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      user_type = request.user.role
      user_profile = User.objects.get(user_type) # experiencing an error here
      
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

# Holding Page pending account approval
def registration_success(request):
    return render(request, 'app/registration_success.html')