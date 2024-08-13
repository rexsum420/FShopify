from django.db import models
from django.conf import settings
from products.models import Product
from shipping.models import ShippingAddress, Tracking
from django.db.models.signals import post_save
from django.dispatch import receiver
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
import stripe


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered')])
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.DO_NOTHING, null=True, blank=True)
    tracking = models.ForeignKey(Tracking, on_delete=models.DO_NOTHING, blank=True, null=True)
    payment_released = models.BooleanField(default=False)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

@receiver(post_save, sender=Order)
def trigger_payment_release(sender, instance, **kwargs):
    if instance.tracking and not instance.payment_released:
        release_payment.delay(instance.id)

@shared_task
def release_payment(order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.tracking and not order.payment_released:
            # Implement the Stripe payment release logic here
            stripe.Transfer.create(
                amount=int(order.total_amount * 100),  # Stripe amount is in cents
                currency="usd",
                destination=order.product.first().store.stripe_account_id,  # Assume each product belongs to the same store
                transfer_group=f"ORDER_{order.id}"
            )
            order.payment_released = True
            order.save()
    except ObjectDoesNotExist:
        # Handle the case where the order does not exist
        pass
