# Generated by Django 3.1.7 on 2021-08-13 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_car_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardealer',
            name='state',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
