from django.contrib.auth.models import User
from django.db import models
from django.apps import apps


# Create your models here.
from backend.models.Task import Task
from backend.models.Topic import Topic


class TopicComment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name="topic_comment_creator", on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name="topic", on_delete=models.CASCADE)