from django.contrib import admin
from .models import Category, Tag, Product, Picture

admin.site.register([Category, Tag, Product, Picture])