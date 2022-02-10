from django.contrib.auth.models import User
from django.db import models

# Create your models here.

from backend.models.Ticket import Ticket


class TicketComment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name="ticket_comment_creator", on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, related_name="ticket", on_delete=models.CASCADE)