# Generated by Django 3.1 on 2020-08-27 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20200827_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='url',
        ),
    ]