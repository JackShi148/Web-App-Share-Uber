# Generated by Django 4.1.5 on 2023-01-31 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_driverinfo_phone_alter_riderinfo_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverinfo',
            name='car_type',
            field=models.CharField(choices=[('Sedan', 'Sedan'), ('SUV', 'SUV')], max_length=10, verbose_name='car_type'),
        ),
    ]