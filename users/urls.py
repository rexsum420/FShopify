from django.urls import path
from .views import reset_password, reset_password_link, login_view, register, logout_view

urlpatterns = [
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset-password'),
    path('reset-password-link/', reset_password_link, name='reset-password-link'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
]