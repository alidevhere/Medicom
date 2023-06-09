# Generated by Django 3.1.2 on 2020-11-09 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=100)),
                ('phone_no', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=True)),
                ('amount', models.FloatField()),
                ('total_items', models.PositiveSmallIntegerField()),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_pharmacy.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50)),
                ('generic_name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='')),
                ('manufacturer', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('inj', 'Injection'), ('tab', 'tablet'), ('syrp', 'syrup'), ('cap', 'capsule'), ('drp', 'drops'), ('inhl', 'inhalers')], max_length=4)),
                ('item_qty', models.IntegerField(default=1)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('purchase_date', models.DateTimeField()),
                ('manufacture_date', models.DateTimeField()),
                ('exp_date', models.DateTimeField()),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_pharmacy.products')),
            ],
        ),
        migrations.CreateModel(
            name='Order_items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_pharmacy.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_pharmacy.products')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery_Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deliver_addr', models.CharField(max_length=100)),
                ('deliver_phn', models.CharField(max_length=20)),
                ('deliver_name', models.CharField(max_length=20)),
                ('deliver_status', models.CharField(choices=[('pen', 'pending'), ('proc', 'process started'), ('delv', 'on the way')], max_length=4)),
                ('deliver_date', models.DateTimeField()),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_pharmacy.customer')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_pharmacy.order')),
            ],
        ),
    ]
