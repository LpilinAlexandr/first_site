# Generated by Django 3.1 on 2020-08-19 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200819_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='group',
            field=models.CharField(choices=[('fruit', 'fruit'), ('vegetable', 'vegetable')], default='fruit', max_length=20),
        ),
    ]
