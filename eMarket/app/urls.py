from django.urls import path
from . import views

urlpatterns = [
  # Root URL
  path('', views.login, name='login'),
  
  # Product URLs
  path('product/', views.product_list, name='product_list'),
  #path('product/<int:product_id>/', views.product_detail, name='product_detail'),
  
  # Account Management URL
  path('register/', views.register, name='register'),
  path('registration_success/', views.registration_success, name='registration_success'),
  path('logout/', views.logout_view, name='logout'),
  
  #Order History URL
  
  #Cart URL
  
]
