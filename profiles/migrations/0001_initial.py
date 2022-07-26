# Generated by Django 3.2.6 on 2022-07-18 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(default='', max_length=256)),
                ('location', models.CharField(default='', max_length=128)),
                ('image', models.ImageField(default='', upload_to='profile_images/')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
    ]