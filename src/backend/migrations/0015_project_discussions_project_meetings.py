# Generated by Django 4.0 on 2022-01-01 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_project_faq_project_resources_project_schema'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='discussions',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='meetings',
            field=models.BooleanField(default=False),
        ),
    ]
