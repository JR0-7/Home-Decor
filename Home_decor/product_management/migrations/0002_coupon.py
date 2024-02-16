# Generated by Django 5.0.1 on 2024-02-15 09:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=100)),
                ('is_expired', models.BooleanField(default=False)),
                ('discount_percentage', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('minimum_amount', models.IntegerField(default=400)),
                ('max_uses', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('expire_date', models.DateField()),
            ],
        ),
    ]
