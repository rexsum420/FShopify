from django.contrib import admin
from .models import Coupon, UsedCoupon, ProductCoupon

admin.site.register([Coupon, UsedCoupon, ProductCoupon])