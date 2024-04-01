# Generated by Django 4.2.2 on 2024-03-15 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0042_customuser_is_blacklisted'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('serviceapp', '0007_delivery_rent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(null=True)),
                ('rating', models.IntegerField(default=0, null=True)),
                ('status', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.product')),
                ('userprofile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]