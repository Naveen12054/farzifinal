# Generated by Django 4.2.2 on 2023-10-08 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_order_product_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
