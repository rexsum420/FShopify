from django.db import models
from django.contrib.auth import get_user_model
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible
from django.core.files.storage import default_storage
User = get_user_model()

@deconstructible
class PathAndRename:
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if self.sub_path == 'logo':
            filename = f'logo.{ext}'
        elif self.sub_path == 'banner':
            filename = f'banner.{ext}'
        else:
            filename = f'{uuid4().hex}.{ext}'

        return os.path.join('brand', str(instance.id), self.sub_path, filename)

class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="store")
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    logo = models.ImageField(upload_to=PathAndRename('logo'), blank=True, null=True)
    banner = models.ImageField(upload_to=PathAndRename('banner'), blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_store = Store.objects.get(pk=self.pk)
            if self.logo != old_store.logo and old_store.logo.name:
                default_storage.delete(old_store.logo.name)
            if self.banner != old_store.banner and old_store.banner.name:
                default_storage.delete(old_store.banner.name)

        if not self.pk and self.owner.role == 'customer':
            self.owner.role = 'store_owner'
            self.owner.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name