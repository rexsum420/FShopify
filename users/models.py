from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('store_owner', 'Store Owner'),
        ('customer', 'Customer'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    ip_addres = models.GenericIPAddressField()

    # Ensure the username is always lowercase and without spaces
    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.lower().replace(" ", "")
        super().save(*args, **kwargs)
