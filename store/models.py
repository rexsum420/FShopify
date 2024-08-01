from django.db import models
from django.contrib.auth import get_user_model
import os
from django.utils.deconstruct import deconstructible
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from uuid import uuid4

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

        return os.path.join('brand', 'temp', filename)

class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="store")
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    logo = models.ImageField(upload_to=PathAndRename('logo'), blank=True, null=True)
    banner = models.ImageField(upload_to=PathAndRename('banner'), blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_logo_name = None
        old_banner_name = None

        if not is_new:
            old_store = Store.objects.get(pk=self.pk)
            old_logo_name = old_store.logo.name if old_store.logo else None
            old_banner_name = old_store.banner.name if old_store.banner else None

        super().save(*args, **kwargs)

        if is_new:
            updated = False
            
            if not self.pk and self.owner.role == 'customer':
                self.owner.role = 'store_owner'
                self.owner.save()

            if self.logo and 'temp/' in self.logo.name:
                ext = self.logo.name.split('.')[-1]
                new_logo_name = f'brand/{self.pk}/logo.{ext}'
                self.logo.name = self._move_file(self.logo, new_logo_name)
                updated = True

            if self.banner and 'temp/' in self.banner.name:
                ext = self.banner.name.split('.')[-1]
                new_banner_name = f'brand/{self.pk}/banner.{ext}'
                self.banner.name = self._move_file(self.banner, new_banner_name)
                updated = True

            if updated:
                super().save(update_fields=['logo', 'banner'])

        else:
            if self.logo and old_logo_name and old_logo_name != self.logo.name:
                default_storage.delete(old_logo_name)

            if self.banner and old_banner_name and old_banner_name != self.banner.name:
                default_storage.delete(old_banner_name)

    def _move_file(self, field_file, new_name):
        file_content = field_file.read()
        default_storage.save(new_name, ContentFile(file_content))
        default_storage.delete(field_file.name)

        return new_name

    def __str__(self):
        return self.name
