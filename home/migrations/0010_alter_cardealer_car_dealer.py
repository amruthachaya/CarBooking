# Generated by Django 4.2.2 on 2023-07-05 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0009_alter_cardealer_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardealer',
            name='car_dealer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]