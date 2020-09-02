# Generated by Django 3.1 on 2020-08-27 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20200825_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=150, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='detailsorder',
            name='payment_state',
            field=models.CharField(max_length=100, verbose_name='Итоговая сумма'),
        ),
    ]