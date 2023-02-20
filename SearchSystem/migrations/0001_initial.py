# Generated by Django 4.0.3 on 2022-08-21 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=1000, unique=True, verbose_name='路径')),
                ('name', models.CharField(max_length=300, unique=True, verbose_name='图片名')),
                ('tags', models.CharField(max_length=200, verbose_name='标签')),
            ],
            options={
                'verbose_name_plural': '图片',
            },
        ),
    ]
