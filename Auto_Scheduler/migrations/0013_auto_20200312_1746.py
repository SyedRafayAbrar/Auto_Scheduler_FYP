# Generated by Django 3.0.2 on 2020-03-12 17:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Auto_Scheduler', '0012_module_date_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp_Module',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField(default=datetime.datetime(2020, 3, 12, 17, 46, 55, 29125))),
            ],
            options={
                'db_table': 'Temp_Module',
            },
        ),
        migrations.AlterField(
            model_name='module',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 12, 17, 46, 55, 28001)),
        ),
        migrations.CreateModel(
            name='Temp_Courses_Module',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('assignedTime', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Auto_Scheduler.Day_Time')),
                ('assigned_room', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Auto_Scheduler.Rooms')),
                ('course', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Auto_Scheduler.Courses')),
                ('module', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Auto_Scheduler.Temp_Module')),
                ('selectedProfessor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Auto_Scheduler.Professors')),
            ],
            options={
                'db_table': 'Temp_Courses_Module',
            },
        ),
    ]
