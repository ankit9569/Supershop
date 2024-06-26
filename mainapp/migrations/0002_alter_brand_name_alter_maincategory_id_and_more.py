# Generated by Django 5.0.3 on 2024-04-09 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='maincategory',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
