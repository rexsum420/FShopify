from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from products.models import Product, Tag

User = get_user_model()

class Analytic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    views = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}: {self.tag.name} - {self.views}'
