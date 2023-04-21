# Generated by Django 3.1.2 on 2021-03-06 05:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_pharmacy', '0018_auto_20210306_1027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requested_order',
            options={'verbose_name': 'Requested Order', 'verbose_name_plural': 'Requested Orders'},
        ),
        migrations.AddField(
            model_name='requested_order',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 6, 10, 42, 33, 219728), verbose_name='Order Date'),
        ),
    ]
