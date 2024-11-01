from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('product_list/', views.product_list, name='product_list'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('add_product/', views.add_product, name='add_product'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('add_to_cart/<product_id>', views.add_to_cart, name = 'add_to_cart'),
    path('remove_from_cart/<product_id>', views.remove_from_cart, name = 'remove_from_cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('cart_checkout/', views.cart_checkout, name ='cart_checkout'),
    path('payment_confirmation/', views.payment_confirmed, name='payment_confirmation'),
    path('order_history/', views.order_history, name='order_history'),
    path('logout/', views.logout_view, name='logout'),
    
]
