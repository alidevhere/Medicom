# Generated by Django 3.1.2 on 2021-01-09 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_pharmacy', '0009_auto_20210109_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='join_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]