# Generated by Django 4.0 on 2021-12-18 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_project_github'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='devwebsite',
            field=models.URLField(blank=True),
        ),
    ]