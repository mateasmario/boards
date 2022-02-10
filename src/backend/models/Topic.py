from django.contrib.auth.models import User
from django.db import models

# Create your models here.

from backend.models.Category import Category

class Topic(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    creator = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="category", on_delete=models.CASCADE)
    pinned = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)