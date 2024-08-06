from django.contrib import admin
from .models import CreditCard, BillingAddress

admin.site.register([CreditCard, BillingAddress])