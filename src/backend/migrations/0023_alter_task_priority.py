# Generated by Django 4.0 on 2022-01-14 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0022_ticket_ticketcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('H', 'High'), ('E', 'Extremely High')], default='S', max_length=1),
        ),
    ]