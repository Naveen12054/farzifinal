# Generated by Django 4.2.2 on 2024-02-08 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0041_customuser_c2c_customuser_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_blacklisted',
            field=models.BooleanField(default=False),
        ),
    ]