# Generated by Django 3.2.6 on 2021-08-19 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_rename_subtopic_problem_sub_topic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='sub_topic',
            new_name='sub_topics',
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=30)),
                ('problems', models.ManyToManyField(to='topics.Problem')),
            ],
        ),
    ]