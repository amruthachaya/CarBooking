# Generated by Django 4.2.2 on 2023-07-27 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_car_vehicle_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='vehicle_number',
        ),
    ]