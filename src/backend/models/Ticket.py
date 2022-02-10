from django.contrib.auth.models import User
from django.db import models

# Create your models here.

from backend.models.Project import Project


class Ticket(models.Model):
    issuer = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.TextField()
    open = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)