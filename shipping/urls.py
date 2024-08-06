from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_shipping, name='create-shipping'),
    path('select', views.select_shipping, name='select-shipping'),
]
