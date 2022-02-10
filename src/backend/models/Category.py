from django.db import models

# Create your models here.
from backend.models.Project import Project


class Category(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)