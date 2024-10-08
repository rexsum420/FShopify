# Generated by Django 5.0.7 on 2024-08-11 04:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('creditcards', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='credit_card',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='creditcards.creditcard'),
        ),
    ]
