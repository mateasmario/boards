from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import requests

from backend.models.Project import Project

from backend.views.HelperFunctions import *

def index_view(request): # ../
    return redirect('/projects')

@login_required
def project_list_view(request): # ../projects/
    ownedProjects = Project.objects.filter(owner=request.user)
    moderatingProjects = Project.objects.filter(mods=request.user)
    workingOnProjects = Project.objects.filter(members=request.user)

    context = {
        'ownedProjects': ownedProjects,
        'moderatingProjects': moderatingProjects,
        'workingOnProjects': workingOnProjects,
    }

    return render(request, "projects/project_list_template.html", context)

@login_required
def project_individual_view(request, projectPK): # ../projects/<int:projectPK>
    if isMember(projectPK, request.user) == True:
        project = Project.objects.get(pk=projectPK)
        data = [i for i in range(50)]
        context = {
            'project': project,
            'data': data,
            'isOwner': isOwner(projectPK, request.user),
            'isMod': isMod(projectPK, request.user),
        }
        return render(request, "projects/project_individual_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't view that project.")
        return redirect('/projects')

@login_required
def project_create_view(request): # ../projects/create/
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        averageNoPeople = request.POST['averageNoPeople']
        github = request.POST['github']
        devwebsite = request.POST['devwebsite']
        owner = request.user

        if Project.objects.filter(title=title, owner=owner).exists():
            deleteMessages(request)
            messages.add_message(request, messages.ERROR, "Project with the same name already exists in your account.")
            return redirect("/projects/create")
        else:
            if github != "" and isGitHubURL(github) == False:
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "The URL you typed in is not a valid GitHub repo link.")
                return redirect("/projects/create")
            else:
                Project.objects.create(title=title, description=description, averageNoPeople=averageNoPeople, github=github, devwebsite=devwebsite, owner=owner)
                deleteMessages(request)
                messages.add_message(request, messages.SUCCESS, "Project '" + title + "' was created.")
                return redirect("/projects")
    else:
        return render(request, "projects/project_create_template.html")

@login_required # ../projects/<int:pk>/update/
def project_update_view(request, projectPK):
    if isOwner(projectPK, request.user) == True:
        if request.method == "POST":
            title = request.POST['title']
            description = request.POST['description']
            averageNoPeople = request.POST['averageNoPeople']
            github = request.POST['github']
            devwebsite = request.POST['devwebsite']
            if github != "" and isGitHubURL(github) == False:
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "The URL you typed in is not a valid GitHub repo link.")
                return redirect("/projects/" + str(projectPK) + "/update")
            else:
                Project.objects.filter(pk=projectPK).update(title=title, description=description, averageNoPeople=averageNoPeople, devwebsite=devwebsite, github=github)
                deleteMessages(request)
                messages.add_message(request, messages.SUCCESS, "Project '" + title + "' has been updated.")
                return redirect('/projects/' + str(projectPK))
        else:
            project = Project.objects.get(pk=projectPK)
            context = {
                'project': project,
                'isOwner': isOwner(projectPK, request.user),
                'isMod': isMod(projectPK, request.user),
            }
            return render(request, "projects/project_update_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't edit that project.")
        return redirect('/projects')

@login_required # ../projects/<int:projectPK>/delete/
def project_delete_view(request, projectPK):
    if isOwner(projectPK, request.user) == True:
        Project.objects.filter(pk=projectPK).delete()
        deleteMessages(request)
        messages.add_message(request, messages.SUCCESS, "You have successfully deleted the project.")
        return redirect('/projects')
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You are not the owner of this project.")
        return redirect('/projects')

@login_required # ../projects/<int:projectPK>/invite/
def project_invite_view(request, projectPK):
    if isMod(projectPK, request.user) == True:
        username = request.POST['username']
        if not User.objects.filter(username=username).exists():
            deleteMessages(request)
            messages.add_message(request, messages.ERROR, "The user you typed in doesn't exist.")
            return redirect('/projects/' + str(projectPK))
        user = User.objects.get(username=username)
        if (isMember(projectPK, user) == True):
            deleteMessages(request)
            messages.add_message(request, messages.ERROR, "User is already part of the project.")
            return redirect('/projects/' + str(projectPK))
        else:
            project = Project.objects.get(pk=projectPK)
            project.members.add(user)
            messages.add_message(request, messages.INFO, "User has been added to the project.")
            return redirect('/projects/' + str(projectPK))
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You don't have enough permissions to invite users to this project.")
        return redirect('/projects/' + str(projectPK))

@login_required # ../projects/<int:projectPK>/members/
def project_members_view(request, projectPK):
    if isMember(projectPK, request.user):
        project = Project.objects.get(pk=projectPK)
        context = {
            'project': project,
            'isOwner': isOwner(projectPK, request.user),
            'isMod': isMod(projectPK, request.user),
        }
        return render(request, "projects/project_members_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't view that project.")
        return redirect('/projects')

@login_required # ../projects/<int:projectPK>/github
def project_github_view(request, projectPK):
    if isMember(projectPK, request.user):
        project = Project.objects.get(pk=projectPK)

        if project.github != "":
            headers = {
                'Accept': 'application/vnd.github.v3+json',
            }

            urlList = project.github.split("/")
            url = ""
            url += urlList[-2]
            url += "/"
            url += urlList[-1]

            response = requests.get('https://api.github.com/repos/' + url, auth=('mateasmario', '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'), headers=headers)
            github = response.json()

            context = {
                'project': project,
                'isOwner': isOwner(projectPK, request.user),
                'isMod': isMod(projectPK, request.user),
                'github': github,
            }
            return render(request, "projects/project_github_template.html", context)
        else:
            deleteMessages(request)
            messages.add_message(request, messages.ERROR, "The project doesn't have any GitHub repo added.")
            return redirect('/projects/' + str(projectPK))
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't view that project.")
        return redirect('/projects')
