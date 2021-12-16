from django.contrib import admin

# Register your models here.
from backend.models.Project import Project
from backend.models.Task import Task

admin.site.register(Project)
admin.site.register(Task)