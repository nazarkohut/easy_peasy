# Generated by Django 3.2.6 on 2021-08-26 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0019_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='problem',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='problem', to='topics.problem'),
        ),
    ]