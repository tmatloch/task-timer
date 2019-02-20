# Generated by Django 2.1.7 on 2019-02-20 23:18

from django.db import migrations, models
from datetime import timedelta


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20190220_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='duration',
            field=models.DurationField(default=timedelta(seconds=0)),
        ),
        migrations.AddField(
            model_name='task',
            name='is_running',
            field=models.BooleanField(default=False),
        ),
    ]
