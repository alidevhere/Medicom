# Generated by Django 3.1.2 on 2021-03-10 07:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_pharmacy', '0023_auto_20210310_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 10, 12, 12, 45, 407274), verbose_name='Order Date'),
        ),
    ]