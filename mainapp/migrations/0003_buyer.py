# Generated by Django 5.0.3 on 2024-04-10 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_brand_name_alter_maincategory_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=30)),
                ('address', models.TextField(blank=True, default='', null=True)),
                ('pin', models.IntegerField(blank=True, default='', null=True)),
                ('city', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('state', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('pic', models.ImageField(blank=True, default='', null=True, upload_to='uploads/users')),
            ],
        ),
    ]
