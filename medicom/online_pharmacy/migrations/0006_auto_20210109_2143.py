# Generated by Django 3.1.2 on 2021-01-09 16:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_pharmacy', '0005_auto_20210109_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='join_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 9, 21, 43, 33, 239432)),
        ),
    ]
