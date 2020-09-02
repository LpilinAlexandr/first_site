# Generated by Django 3.1 on 2020-08-09 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=70, verbose_name='Имя пользователя')),
                ('birthday', models.DateTimeField(verbose_name='День рождения')),
            ],
        ),
    ]
