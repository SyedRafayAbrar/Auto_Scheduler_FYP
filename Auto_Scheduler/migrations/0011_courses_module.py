# Generated by Django 3.0.2 on 2020-03-08 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Auto_Scheduler', '0010_remove_module_date_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses_Module',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('assignedTime', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Auto_Scheduler.Day_Time')),
                ('assigned_room', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Auto_Scheduler.Rooms')),
                ('course', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Auto_Scheduler.Courses')),
                ('module', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Auto_Scheduler.Module')),
                ('selectedProfessor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Auto_Scheduler.Professors')),
            ],
            options={
                'db_table': 'Courses_Module',
            },
        ),
    ]