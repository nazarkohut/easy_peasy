# Generated by Django 3.2.6 on 2021-08-26 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0015_alter_task_problem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='problem',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related', to='topics.problem'),
        ),
    ]
