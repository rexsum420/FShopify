from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Coupon(models.Model):
    COUPON_TYPE_CHOICES = [
        ('general', 'General'),
        ('product', 'Product-specific'),
    ]

    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    expires_at = models.DateTimeField()
    coupon_type = models.CharField(max_length=10, choices=COUPON_TYPE_CHOICES, default='product')

class ProductCoupon(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='product_coupons')

class UsedCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
