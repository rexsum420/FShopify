# Generated by Django 5.0.7 on 2024-08-11 04:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('analytics', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='analytic',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.tag'),
        ),
    ]
