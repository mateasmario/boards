# Generated by Django 4.0 on 2022-01-01 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_task_commit'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='forums',
            field=models.BooleanField(default=False),
        ),
    ]
