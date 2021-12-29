from django.contrib.auth.models import User
from django.db import models
from django.apps import apps


# Create your models here.
from backend.models.Task import Task


class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name="task", on_delete=models.CASCADE)