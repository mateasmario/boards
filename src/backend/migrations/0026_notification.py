# Generated by Django 4.0 on 2022-01-19 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('backend', '0025_ticket_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('TA', 'Task Assignment'), ('PI', 'Project Invitation'), ('PK', 'Project Kick'), ('TA', 'Ticket Answer')], default='TA', max_length=2)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('project', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_project', to='backend.project')),
                ('task', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_task', to='backend.task')),
                ('ticket', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_ticket', to='backend.ticket')),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]