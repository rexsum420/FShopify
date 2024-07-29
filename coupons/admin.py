from django.contrib import admin
from .models import Coupon, UserCoupon, ProductCoupon

admin.site.register([Coupon, UserCoupon, ProductCoupon])