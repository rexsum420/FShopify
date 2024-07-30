# Generated by Django 5.0.7 on 2024-07-29 22:33

import django.db.models.deletion
import products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_category_parent_remove_product_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=products.models.product_picture_upload_to)),
                ('alt', models.CharField(max_length=256)),
                ('main', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='products.product')),
            ],
        ),
    ]
