# Generated by Django 2.1.7 on 2019-02-25 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20190221_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='end_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
    ]