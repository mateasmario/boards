from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Project(models.Model):
    # Basic information
    title = models.CharField(max_length=128)
    description = models.TextField()
    averageNoPeople = models.IntegerField()
    github = models.URLField(blank=True)
    devwebsite = models.URLField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    # User management
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    mods = models.ManyToManyField(User, related_name="mods")
    members = models.ManyToManyField(User, related_name="members")

    # Add-ons
    forums = models.BooleanField(default=False)
    contact_page = models.BooleanField(default=False)
    resources = models.BooleanField(default=False)
    faq = models.BooleanField(default=False)
    schema = models.BooleanField(default=False)
    meetings = models.BooleanField(default=False)
    discussions = models.BooleanField(default=False)