# Generated by Django 3.1 on 2020-08-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200818_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
