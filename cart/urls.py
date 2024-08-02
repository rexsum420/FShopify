from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('', views.cart_detail, name='cart_detail'),
]
