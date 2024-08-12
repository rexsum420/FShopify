from django.db import models
from django.conf import settings
from orders.models import Order
from django.contrib.auth import get_user_model
User = get_user_model()

class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')])
    created_at = models.DateTimeField(auto_now_add=True)


class Dispute(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
