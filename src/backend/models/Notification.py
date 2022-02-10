from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from backend.models.Project import Project
from backend.models.Task import Task
from backend.models.Ticket import Ticket


class Notification(models.Model):
    TYPE = (
        ('TA', 'Task Assignment'),
        ('TC', 'Task Assignee Change'),
        ('TU', 'Task Update'),
        ('PI', 'Project Invitation'),
        ('TA', 'Ticket Answer'),
    )
    type = models.CharField(max_length=2, choices=TYPE, default='TA')

    date = models.DateTimeField(auto_now_add=True)
    to = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    # Task Assignment
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="notification_task", blank=True, null=True)

    # Project Invitation / Project Kick / Task Assignment / Task Update
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="notification_project", blank=True, null=True)

    # Ticket Answer
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="notification_ticket", blank=True, null=True)