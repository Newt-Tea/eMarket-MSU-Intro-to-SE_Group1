from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('product_list/', views.product_list, name='product_list'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('add_to_cart/<product_id>/', views.add_to_cart, name = 'add_to_cart'),
    path('update_cart_quantity/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('payment_confirmation/', views.payment_confirmed, name='payment_confirmation'),
    path('order_history/', views.order_history, name='order_history'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order_return/<int:order_id>/', views.order_return, name='order_return'),
    path('order_return_success/', views.order_return_success, name='order_return_success'),
    path('logout/', views.logout_view, name='logout'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller_dashboard/create_product/', views.create_product, name='create_product'),
    path('seller_dashboard/remove_product/<int:product_id>/', views.remove_product, name='remove_product'),
    path('update_stock/<int:product_id>/', views.update_stock, name='update_stock'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_list/',views.user_list, name='user_list'),
    path('admin_product_list/', views.admin_product_list, name='admin_product_list')
]
