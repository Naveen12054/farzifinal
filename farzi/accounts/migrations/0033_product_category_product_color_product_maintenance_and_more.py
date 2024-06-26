# Generated by Django 4.2.2 on 2023-09-21 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_remove_product_category_remove_product_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=34, on_delete=django.db.models.deletion.CASCADE, related_name='cat', to='accounts.category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='maintenance',
            field=models.CharField(max_length=555, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='material_description',
            field=models.TextField(max_length=555, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='measurements',
            field=models.CharField(max_length=555, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_description',
            field=models.TextField(max_length=555, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_images1',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='sample/'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_images2',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='sample/'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_images3',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='sample/'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_images4',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='sample/'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.BooleanField(default=False, max_length=555),
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, related_name='cat1', to='accounts.subcategory'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
