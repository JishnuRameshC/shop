# Generated by Django 4.2.1 on 2023-06-01 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_customer_alter_order_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total_price',
        ),
    ]
