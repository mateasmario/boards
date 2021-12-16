from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    mods = models.ManyToManyField(User, related_name="mods")
    members = models.ManyToManyField(User, related_name="members")