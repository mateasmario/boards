# Generated by Django 4.0 on 2022-01-04 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_topic_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='pinned',
            field=models.BooleanField(default=False),
        ),
    ]
