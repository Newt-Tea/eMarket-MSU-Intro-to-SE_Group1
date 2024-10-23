from django.shortcuts import render
from .models import Product, Cart, Order

#TO-DO Product Page
def product_list(request):
  print("Not Implemented")
  print(f"Request = {request}")

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import User
from .forms import UserCreationForm, UserLoginForm 

def login_view(request):
  if request.method == 'POST':
    form = UserLoginForm(request, data = request.POST)
    if form.is_valid():
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(request, username=username, password=password)

      if user is not None:
        login(request, user)
        user_profile = User.objects.get(user=user)
        
        # Redirect based on user type
        if user_profile.user_type == 'admin':
          return redirect('admin_dashboard')
        elif user_profile.user_type == 'seller':
          return redirect('seller_dashboard')
        #else:
          return redirect('product_list')
    else:
      form = UserLoginForm()

  return render(request, 'app/login.html')


