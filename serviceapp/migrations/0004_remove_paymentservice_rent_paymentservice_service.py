# Generated by Django 4.2.2 on 2024-03-13 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0037_rename_condition_furniturerent_stock'),
        ('serviceapp', '0003_paymentservice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentservice',
            name='rent',
        ),
        migrations.AddField(
            model_name='paymentservice',
            name='service',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='rest.appointment'),
        ),
    ]
