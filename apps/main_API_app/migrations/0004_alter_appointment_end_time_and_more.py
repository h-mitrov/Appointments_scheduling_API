# Generated by Django 4.0.5 on 2022-06-23 13:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_API_app', '0003_appointment_date_alter_appointment_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2022, 6, 23, 17, 57, 33, 609513)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_API_app.location'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='start_time',
            field=models.TimeField(default=datetime.time(16, 57, 33, 609513)),
        ),
    ]
