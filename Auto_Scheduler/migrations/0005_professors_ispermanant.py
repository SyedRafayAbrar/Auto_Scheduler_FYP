# Generated by Django 3.0.2 on 2020-03-05 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auto_Scheduler', '0004_remove_users_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='professors',
            name='isPermanant',
            field=models.BooleanField(default=False),
        ),
    ]