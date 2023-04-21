# Generated by Django 3.1.2 on 2021-03-07 08:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_pharmacy', '0020_auto_20210307_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='prescription_img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 7, 13, 12, 50, 684936), verbose_name='Order Date'),
        ),
    ]