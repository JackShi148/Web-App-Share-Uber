# Generated by Django 4.1.5 on 2023-02-04 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0009_alter_ride_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='vehicle_type',
            field=models.CharField(choices=[('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Coupe', 'Coupe'), ('Van', 'Van')], max_length=10),
        ),
    ]
