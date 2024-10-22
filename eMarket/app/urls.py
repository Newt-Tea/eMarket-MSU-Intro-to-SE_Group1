from django.urls import path
from . import views

urlpatterns = [
  path('product_list/', views.product_list, name='product_list'),
  #path('product/<int:product_id>/', views.product_detail, name='product_detail'),
  path('', views.login, name='login'),
  path('register/', views.register, name='register'),
  path('registration_success/', views.registration_success, name='registration_success'),
  #path('logout/', views.logout_view, name='logout'),
]
