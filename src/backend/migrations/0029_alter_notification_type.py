# Generated by Django 4.0 on 2022-01-19 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0028_alter_notification_project_alter_notification_task_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('TA', 'Task Assignment'), ('TU', 'Task Update'), ('TD', 'Task Deletion'), ('PI', 'Project Invitation'), ('PK', 'Project Kick'), ('TA', 'Ticket Answer')], default='TA', max_length=2),
        ),
    ]
