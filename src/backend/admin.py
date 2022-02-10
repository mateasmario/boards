from django.contrib import admin

# Register your models here.
from backend.models.Category import Category
from backend.models.Project import Project
from backend.models.Task import Task
from backend.models.TaskComment import TaskComment
from backend.models.Ticket import Ticket
from backend.models.TicketComment import TicketComment
from backend.models.Topic import Topic
from backend.models.TopicComment import TopicComment
from backend.models.Notification import Notification

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(TopicComment)
admin.site.register(Ticket)
admin.site.register(TicketComment)
admin.site.register(Notification)
