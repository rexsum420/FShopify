from django.db import models
from store.models import Store
import uuid
from django.utils.deconstruct import deconstructible
from django.conf import settings
import boto3

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name

@deconstructible
class PathAndRename:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f'{uuid.uuid4()}.{ext}'
        return f'{self.path}/{filename}'

def product_picture_upload_to(instance, filename):
    return PathAndRename('products/pictures/')(instance, filename)
    
class Picture(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(upload_to=product_picture_upload_to)
    alt = models.CharField(max_length=256, default='')
    main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.main:
            super().save(*args, **kwargs)
            pics = Picture.objects.filter(product=self.product).exclude(id=self.id)
            for pic in pics:
                if pic.main:
                    pic.main = False
                    pic.save()
        else:
            super().save(*args, **kwargs)
            pics = Picture.objects.filter(product=self.product)
            if len(pics) == 1:
                pics[0].main = True
                pics[0].save()

    def delete(self, *args, **kwargs):
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=self.image.name)
        
        # Call the parent class delete method
        super().delete(*args, **kwargs)