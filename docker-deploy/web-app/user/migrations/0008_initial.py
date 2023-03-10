# Generated by Django 4.1.5 on 2023-01-30 23:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0007_remove_riderinfo_user_ptr_delete_driverinfo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiderInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField(verbose_name='phone')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DriverInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10, verbose_name='phone')),
                ('car_type', models.SmallIntegerField(choices=[(1, 'Sedan'), (2, 'SUV')], verbose_name='car_type')),
                ('licenseNum', models.CharField(max_length=100, verbose_name='licenseNum')),
                ('plateNum', models.CharField(max_length=100, verbose_name='licenseNum')),
                ('max_pgers', models.IntegerField(verbose_name='max_pgers')),
                ('special_info', models.CharField(max_length=30, verbose_name='username')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
