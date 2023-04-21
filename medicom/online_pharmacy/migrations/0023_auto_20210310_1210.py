# Generated by Django 3.1.2 on 2021-03-10 07:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_pharmacy', '0022_auto_20210310_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 10, 12, 10, 54, 31996), verbose_name='Order Date'),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='prescription_img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
