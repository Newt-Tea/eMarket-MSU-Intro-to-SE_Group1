from django.urls import path
from . import views

urlpatterns = [
  path('', views.product_list, name='product_list'),
  path('login/', views.login_view, name='login'),
  path('product/<int:product_id>/', views.product_list, name='product_detail'),
]
