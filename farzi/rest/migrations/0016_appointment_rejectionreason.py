# Generated by Django 4.2.2 on 2024-02-06 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0015_appointment_approved_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='rejectionreason',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
