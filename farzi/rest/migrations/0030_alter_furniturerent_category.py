# Generated by Django 4.2.2 on 2024-02-21 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0029_furniturerent_rentproduct_alter_furniturerent_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='furniturerent',
            name='category',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
