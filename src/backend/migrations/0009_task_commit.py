# Generated by Django 4.0 on 2021-12-26 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_comment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='commit',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]