# Generated by Django 4.2.2 on 2024-03-13 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0037_rename_condition_furniturerent_stock'),
        ('main', '0026_orderitem_deliverystatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rest.addressuser'),
        ),
    ]
