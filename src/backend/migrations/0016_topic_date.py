# Generated by Django 4.0 on 2022-01-03 21:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_project_discussions_project_meetings'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
