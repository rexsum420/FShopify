from django.db import models

class SEO(models.Model):
    page = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.CharField(max_length=255)
