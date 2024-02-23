# Generated by Django 5.0.1 on 2024-02-18 11:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_order_payment_alter_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='order_product_status',
            field=models.CharField(choices=[('New', 'New'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='New', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='order.order'),
        ),
    ]
