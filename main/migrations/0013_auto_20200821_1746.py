# Generated by Django 3.1 on 2020-08-21 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20200820_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
