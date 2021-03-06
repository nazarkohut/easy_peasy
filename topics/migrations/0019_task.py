# Generated by Django 3.2.6 on 2021-08-26 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0018_delete_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.TextField(max_length=1000)),
                ('problem', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related', to='topics.problem')),
            ],
        ),
    ]
