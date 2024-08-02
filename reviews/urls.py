from django.urls import path
from . import views

urlpatterns = [
    path('create-rating', views.create_rating, name='create-rating'),
    path('create-review', views.create_review, name='create-review'),
]
