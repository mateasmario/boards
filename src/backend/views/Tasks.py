from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from backend.models.Comment import Comment
from backend.views.HelperFunctions import *

@login_required
def task_list_view(request, projectPK): # ../projects/<int:projectPK>/tasks
    if isMember(projectPK, request.user):
        project = Project.objects.get(pk=projectPK)
        myTasks = Task.objects.filter(project=project, assignee=request.user)
        otherTasks = Task.objects.filter(project=project).exclude(assignee=request.user)
        context = {
            'project': project,
            'myTasks': myTasks,
            'otherTasks': otherTasks,
            'isOwner': isOwner(projectPK, request.user),
            'isMod': isMod(projectPK, request.user),
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
            'task': task,
            'comments': Comment.objects.filter(task=task).order_by('date').reverse(),
            'project': Project.objects.get(pk=projectPK),
            'isOwner': isOwner(projectPK, request.user),
            'isMod': isMod(projectPK, request.user),

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
                deleteMessages(request)
                messages.add_message(request, messages.SUCCESS, "Task was created.")
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
                'isOwner': isOwner(projectPK, request.user),
                'isMod': isMod(projectPK, request.user),
                'project': Project.objects.get(pk=projectPK),
            }

            return render(request, "tasks/task_create_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't create a task on this project.")
        return redirect('/projects/' + str(projectPK) + '/tasks')

@login_required
def task_delete_view(request, projectPK, taskPK): # ../projects/<int:projectPK>/tasks/<int:taskPK>/delete
    if taskBelongsToProject(taskPK, projectPK) and (isIssuer(taskPK, request.user) or isMod(projectPK, request.user)):
        Task.objects.filter(pk=taskPK).delete()
        deleteMessages(request)
        messages.add_message(request, messages.SUCCESS, "Task was deleted successfully.")
        return redirect('/projects/' + str(projectPK) + '/tasks')
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You don't have permission to delete this task.")
        return redirect('/projects/' + str(projectPK))

@login_required
def task_mark_solved_view(request, projectPK, taskPK): # ../projects/<int:projectPK>/tasks/<int:taskPK>/mark_solved
    if taskBelongsToProject(taskPK, projectPK) and (isAssignee(taskPK, request.user) or isIssuer(taskPK, request.user) or isMod(projectPK, request.user)):
        Task.objects.filter(pk=taskPK).update(solved=True)
        deleteMessages(request)
        messages.add_message(request, messages.SUCCESS, "Task marked as solved.")
        return redirect('/projects/' + str(projectPK) + '/tasks/' + str(taskPK))
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "Couldn't mark task as solved.")
        return redirect('/projects/' + str(projectPK) + '/tasks')

@login_required
def task_mark_unsolved_view(request, projectPK, taskPK): # ../projects/<int:projectPK>/tasks/<int:taskPK>/mark_unsolved
    if taskBelongsToProject(taskPK, projectPK) and (isAssignee(taskPK, request.user) or isIssuer(taskPK, request.user) or isMod(projectPK, request.user)):
        Task.objects.filter(pk=taskPK).update(solved=False)
        deleteMessages(request)
        messages.add_message(request, messages.SUCCESS, "Task marked as unsolved.")
        return redirect('/projects/' + str(projectPK) + '/tasks/' + str(taskPK))
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "Couldn't mark task as unsolved.")
        return redirect('/projects/' + str(projectPK) + '/tasks')

@login_required
def task_comment_add_view(request, projectPK, taskPK): # ../projects/<int:projectPK>/tasks/<int:taskPK>/comments/add
    if taskBelongsToProject(taskPK, projectPK) and isMember(projectPK, request.user):
        if request.method == "POST":
            content = request.POST['content']
            task = Task.objects.get(pk=taskPK)
            Comment.objects.create(content=content, creator=request.user, task=task)
            deleteMessages(request)
            messages.add_message(request, messages.SUCCESS, "Comment added.")
        else:
            deleteMessages(request)
            messages.add_message(request, messages.ERROR, "Couldn't add comment to the task.")
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "Couldn't add comment to the task.")
    return redirect('/projects/' + str(projectPK) + '/tasks/' + str(taskPK))

@login_required
def task_comment_delete_view(request, projectPK, taskPK, commentPK): # ../projects/<int:projectPK>/tasks/<int:tasPK>/comments/<int:commentPK>/delete
    if taskBelongsToProject(taskPK, projectPK) and isCreator(commentPK, request.user):
        Comment.objects.get(pk=commentPK).delete()
        messages.add_message(request, messages.SUCCESS, "Comment has been deleted.")
        return redirect('/projects/' + str(projectPK) + '/tasks/' + str(taskPK))
    else:
        messages.add_message(request, messages.ERROR, "Could not delete comment.")
        return redirect('/projects/' + str(projectPK) + '/tasks/' + str(taskPK))