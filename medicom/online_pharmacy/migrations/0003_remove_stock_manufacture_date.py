# Generated by Django 3.1.2 on 2020-11-18 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_pharmacy', '0002_auto_20201118_0703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='manufacture_date',
        ),
    ]
