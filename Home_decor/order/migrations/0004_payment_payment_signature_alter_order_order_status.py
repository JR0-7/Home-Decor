# Generated by Django 5.0.1 on 2024-02-10 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_payment_user_payment_is_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('New', 'New'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='New', max_length=20),
        ),
    ]
