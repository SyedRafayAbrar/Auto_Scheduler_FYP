# Generated by Django 3.0.2 on 2020-03-08 06:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auto_Scheduler', '0008_module'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='date_time',
            field=models.CharField(default=datetime.datetime(2020, 3, 8, 6, 2, 11, 773457), max_length=100),
        ),
    ]
