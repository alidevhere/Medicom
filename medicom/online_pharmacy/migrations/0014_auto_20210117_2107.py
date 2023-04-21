# Generated by Django 3.1.2 on 2021-01-17 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_pharmacy', '0013_auto_20210117_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery_details',
            name='deliver_status',
            field=models.CharField(choices=[('pen', 'pending'), ('proc', 'process started'), ('delv', 'on the way')], default='pen', max_length=4, verbose_name='Status'),
        ),
    ]
