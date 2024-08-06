from django.db import models

class ShippingMethod(models.Model):
    name = models.CharField(max_length=255)
    carrier = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class ShippingAddress(models.Model):
    customer_name = models.CharField(max_length=64)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)