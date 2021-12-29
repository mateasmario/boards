# Generated by Django 4.0 on 2021-12-25 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('backend', '0006_comment_task_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='comments',
        ),
        migrations.AddField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='task', to='backend.task'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='auth.user'),
        ),
    ]
