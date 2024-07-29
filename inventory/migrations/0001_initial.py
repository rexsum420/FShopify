# Generated by Django 5.0.7 on 2024-07-28 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('low_stock_threshold', models.PositiveIntegerField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
