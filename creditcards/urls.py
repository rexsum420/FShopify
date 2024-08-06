from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add_credit_card, name='add-credit-card'),
    path('select-payment', views.select_payment, name='select-payment'),
]
