# Generated by Django 4.1.5 on 2023-02-01 02:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0003_rename_arrive_date_ride_arrive_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ride',
            old_name='arrive_time',
            new_name='arrival_time',
        ),
    ]
