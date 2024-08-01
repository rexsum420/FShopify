from django.contrib import admin
from django.urls import path, include
from users.views import UserViewSet
from store.views import StoreViewSet
from products.views import ProductViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'stores', StoreViewSet, basename='store')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/', ObtainAuthToken.as_view()),
    path('users/', include('users.urls')),
    path('stores/', include('store.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('search/', include('search.urls')),
    path('', views.index, name='home'),
]
