from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from backend.views.HelperFunctions import *

@login_required
def task_list_view(request, projectPK): # ../projects/<int:projectPK>/tasks
    if isMember(projectPK, request.user):
        project = Project.objects.get(pk=projectPK)
        tasks = Task.objects.filter(project=project)
        context = {
            'tasks': tasks
        }
        return render(request, "tasks/task_list_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "This project does not exist.")
        return redirect('/projects/' + str(projectPK))

@login_required
def task_individual_view(request, projectPK, taskPK): # ../projects/<int:projectPK>/tasks/<int:taskPK>
    if isMember(projectPK, request.user) and taskExists(taskPK):
        task = Task.objects.get(pk=taskPK)
        context = {
            'task': task
        }
        return render(request, "tasks/task_individual_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't view that task.")
        return redirect('/projects/' + str(projectPK))

@login_required
def task_create_view(request, projectPK): # ../projects/<int:projectPK>/tasks/create
    if isMod(projectPK, request.user):
        if request.method == "POST":
            title = request.POST['title']
            description = request.POST['description']
            priority = request.POST['priority']
            type = request.POST['type']
            issuer = request.user
            assignee = request.POST['assignee']
            if User.objects.filter(username=assignee).exists():
                Task.objects.create(title=title, description=description, priority=priority, type=type, issuer=issuer, assignee=User.objects.get(username=assignee), project=Project.objects.get(pk=projectPK))
            else:
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "The assignee you entered doesn't exist.")
            return redirect('/projects/' + str(projectPK) + '/tasks')
        else:
            owner = Project.objects.get(pk=projectPK).owner
            mods = Project.objects.get(pk=projectPK).mods.all()
            members = Project.objects.get(pk=projectPK).members.all()

            context = {
                'owner': owner,
                'mods': mods,
                'members': members,
            }

            return render(request, "tasks/task_create_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't create a task on this project.")
        return redirect('/projects/' + str(projectPK) + '/tasks')

@login_required
def task_delete_view(request, projectPK, taskPK): # ../projects/<int:projectPK>/tasks/delete/<int:taskPK>
    if isMod(projectPK, request.user):
        Task.objects.filter(pk=taskPK).delete()
        return redirect('/projects/' + str(projectPK) + '/tasks')
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You don't have permission to delete this task.")
        return redirect('/projects/' + str(projectPK))

@login_required
def task_mark_solved_view(request, projectPK, taskPK): # ../projects/<int:projectPK>/tasks/mark_solved/<int:taskPK>
    if taskBelongsToProject(taskPK, projectPK) and isAssignee(taskPK, request.user):
        Task.objects.filter(pk=taskPK).update(solved=True)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "Couldn't mark task as solved.")
        return redirect('/projects/' + str(projectPK) + '/tasks')

@login_required
def task_mark_unsolved_view(request, projectPK, taskPK): # ../projects/<int:projectPK>/tasks/mark_unsolved/<int:taskPK>
    if taskBelongsToProject(taskPK, projectPK) and isAssignee(taskPK, request.user):
        Task.objects.filter(pk=taskPK).update(solved=False)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "Couldn't mark task as unsolved.")
        return redirect('/projects/' + str(projectPK) + '/tasks')