# Generated by Django 3.2.6 on 2021-08-25 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0008_auto_20210825_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='problem',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]