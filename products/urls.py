from django.urls import path
from . import views

urlpatterns = [
    path('create/<str:store_name>/', views.create_product, name='create-product'),
]
