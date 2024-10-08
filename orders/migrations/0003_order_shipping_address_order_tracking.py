# Generated by Django 5.0.7 on 2024-08-12 01:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
        ('shipping', '0003_tracking_delete_shippingmethod'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shipping.shippingaddress'),
        ),
        migrations.AddField(
            model_name='order',
            name='tracking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shipping.tracking'),
        ),
    ]
