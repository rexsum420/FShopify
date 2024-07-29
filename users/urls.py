from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('signout', views.logout_view, name='signout'),
]
