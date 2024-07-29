from django.contrib import admin
from .models import ShippingAddress, ShippingMethod

admin.site.register([ShippingMethod, ShippingAddress])