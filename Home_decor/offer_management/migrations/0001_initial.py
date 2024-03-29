# Generated by Django 5.0.1 on 2024-02-21 05:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category_management', '0001_initial'),
        ('product_management', '0004_usercoupon'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=100)),
                ('expire_date', models.DateField()),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('category_offer_slug', models.SlugField(max_length=200, unique=True)),
                ('category_offer_image', models.ImageField(blank=True, upload_to='media/category_offer/images/')),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category_management.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=100)),
                ('expire_date', models.DateField()),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('product_offer_slug', models.SlugField(max_length=200, unique=True)),
                ('product_offer_image', models.ImageField(blank=True, upload_to='product_offer/images/')),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_management.product')),
            ],
        ),
    ]
