# Generated by Django 4.2.2 on 2023-09-27 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookcart',
            name='quantity',
            field=models.PositiveIntegerField(default=1, null=True),
        ),
    ]
