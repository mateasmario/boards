from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from backend.models.Project import Project


class Task(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()

    PRIORITIES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('H', 'High'),
        ('U', 'Urgent'),
    )
    priority = models.CharField(max_length=1, choices=PRIORITIES, default='S')

    TYPE = (
        ('F', 'Feature'),
        ('B', 'Bug'),
        ('M', 'Modification'),
    )
    type = models.CharField(max_length=1, choices=TYPE, default='F')

    date = models.DateTimeField(auto_now_add=True)
    issuer = models.ForeignKey(User, related_name="issuer", on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name="assignee", on_delete=models.CASCADE)
    solved = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    commit = models.CharField(max_length=64, blank=True)