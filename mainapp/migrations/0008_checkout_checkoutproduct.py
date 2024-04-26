# Generated by Django 5.0.3 on 2024-04-21 21:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_addtocart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('orderstatus', models.IntegerField(choices=[(0, 'Order is Placed'), (1, 'Order is Packed'), (2, 'Ready to Dispatch'), (3, 'Ready to Dispatch'), (4, 'Dispatched'), (5, 'Out for Delivery')], default=0)),
                ('paymentstatus', models.IntegerField(choices=[(0, 'Pending'), (1, 'Done')])),
                ('paymentmode', models.IntegerField(choices=[(0, 'COD'), (1, 'Net Banking')], default=0)),
                ('subtotal', models.IntegerField()),
                ('shipping', models.IntegerField()),
                ('total', models.IntegerField()),
                ('rpid', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.buyer')),
            ],
        ),
        migrations.CreateModel(
            name='CheckoutProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.IntegerField()),
                ('total', models.IntegerField()),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.checkout')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product')),
            ],
        ),
    ]
