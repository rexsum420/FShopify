from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_store, name='create-store'),
    path('<store_name>', views.view_store, name='view_store'),
    path('', views.my_stores, name='my-stores'),
]
