# Generated by Django 4.2.2 on 2023-07-14 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_tracking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracking',
            name='charge',
            field=models.FloatField(default=True),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='device_id',
            field=models.IntegerField(default=0),
        ),
    ]
