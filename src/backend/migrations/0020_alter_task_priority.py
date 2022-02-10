# Generated by Django 4.0 on 2022-01-07 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_alter_task_description_alter_task_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('D', '3 Small'), ('C', '2 Medium'), ('B', '1 High'), ('A', '0 Urgent')], default='S', max_length=1),
        ),
    ]
