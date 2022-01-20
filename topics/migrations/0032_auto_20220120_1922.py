# Generated by Django 3.2.6 on 2022-01-20 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0031_auto_20211229_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='answer',
            field=models.FloatField(max_length=4),
        ),
        migrations.AlterField(
            model_name='problem',
            name='task',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
