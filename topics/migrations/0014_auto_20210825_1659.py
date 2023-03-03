# Generated by Django 3.2.6 on 2021-08-25 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0013_auto_20210825_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='accepted',
            field=models.BigIntegerField(default=None),
        ),
        migrations.AddField(
            model_name='problem',
            name='attempts',
            field=models.BigIntegerField(default=None),
        ),
        migrations.AddField(
            model_name='problem',
            name='complexity',
            field=models.IntegerField(default=None),
        ),
    ]