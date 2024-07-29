from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="store")
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    

    def save(self, *args, **kwargs):
        if not self.pk and self.owner.role == 'customer':
            self.owner.role = 'store_owner'
            self.owner.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
