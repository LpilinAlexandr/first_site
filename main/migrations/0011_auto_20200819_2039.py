# Generated by Django 3.1 on 2020-08-19 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20200819_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_unit_price',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='group',
            field=models.CharField(choices=[('vegetable', 'vegetable'), ('fruit', 'fruit')], default='fruit', max_length=20),
        ),
    ]
