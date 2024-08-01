from django.urls import path
from . import views

urlpatterns = [
    path('create/<str:store_name>', views.create_product, name='create-product'),
    path('view', views.product_detail, name='product-detail'),
    path('edit', views.edit_product, name='edit-product'),
]
