# Generated by Django 4.2.2 on 2023-07-26 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_car_vehicle_number_order_end_time_order_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='vehicle_number',
            field=models.CharField(default=True, max_length=15),
        ),
    ]