from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Coupon, UserCoupon, ProductCoupon
from orders.models import Order, OrderItem
from products.models import Product

def apply_general_coupon(user, order_id, coupon_code):
    coupon = get_object_or_404(Coupon, code=coupon_code, active=True, expires_at__gte=timezone.now(), coupon_type='general')
    
    if UserCoupon.objects.filter(user=user, coupon=coupon).exists():
        raise ValueError("Coupon already used by this user.")

    order = get_object_or_404(Order, id=order_id, user=user)

    discount_amount = order.total_amount * (coupon.discount / 100)
    order.total_amount -= discount_amount
    order.save()

    UserCoupon.objects.create(user=user, coupon=coupon)

def apply_product_coupon(user, order_id, product_id, coupon_code):
    product = get_object_or_404(Product, id=product_id)
    coupon = get_object_or_404(Coupon, code=coupon_code, active=True, expires_at__gte=timezone.now(), coupon_type='product')
    product_coupon = get_object_or_404(ProductCoupon, product=product, coupon=coupon)

    if UserCoupon.objects.filter(user=user, coupon=coupon, product=product).exists():
        raise ValueError("Coupon already used by this user for this product.")

    order = get_object_or_404(Order, id=order_id, user=user)
    order_item = get_object_or_404(OrderItem, order=order, product=product)

    discount_amount = order_item.price * (coupon.discount / 100)
    order_item.price -= discount_amount
    order_item.save()

    order.total_amount -= discount_amount
    order.save()

    UserCoupon.objects.create(user=user, coupon=coupon, product=product)
