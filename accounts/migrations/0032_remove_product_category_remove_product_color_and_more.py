# Generated by Django 4.2.2 on 2023-09-21 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_rename_breadth_product_color_remove_product_height_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='product',
            name='material_description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='measurements',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_images1',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_images2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_images3',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_images4',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='product',
            name='status',
        ),
        migrations.RemoveField(
            model_name='product',
            name='subcategory',
        ),
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
    ]
