# Generated by Django 2.1 on 2019-01-01 07:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 1, 1, 7, 3, 19, 620888, tzinfo=utc)),
        ),
    ]
