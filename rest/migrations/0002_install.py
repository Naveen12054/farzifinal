# Generated by Django 4.2.2 on 2024-01-19 05:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='install',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('price', models.CharField(max_length=12)),
                ('date', models.DateField()),
                ('start_time', models.TimeField(null=True)),
                ('status', models.BooleanField(default=False)),
                ('del_status', models.BooleanField(default=False)),
                ('email', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings_by_email', to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings_by_name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
