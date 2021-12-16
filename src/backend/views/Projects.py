from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from backend.models.Project import Project

from backend.views.HelperFunctions import *

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
        context = {
            'project': project
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
        owner = request.user

        if Project.objects.filter(title=title, owner=owner).exists():
            deleteMessages(request)
            messages.add_message(request, messages.ERROR, "Project with the same name already exists in your account.")
            return redirect("/projects/create")
        else:
            Project.objects.create(title=title, description=description, owner=owner)
            return redirect("/projects")
    else:
        return render(request, "projects/project_create_template.html")

@login_required # ../projects/<int:pk>/update/
def project_update_view(request, projectPK):
    if isOwner(projectPK, request.user) == True:
        if request.method == "POST":
            title = request.POST['title']
            description = request.POST['description']
            Project.objects.filter(pk=projectPK).update(title=title, description=description)
            return redirect('/projects/' + str(projectPK))
        else:
            project = Project.objects.get(pk=projectPK)
            context = {
                'project': project
            }
            return render(request, "projects/project_update_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't edit that project.")
        return redirect('/projects')

@login_required # ../projects/<int:pk>/delete/
def project_delete_view(request, projectPK):
    if isOwner(projectPK, request.user) == True:
        Project.objects.filter(pk=projectPK).delete()
        deleteMessages(request)
        messages.add_message(request, messages.INFO, "You have successfully deleted the project.")
        return redirect('/projects')
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You are not the owner of this project.")
        return redirect('/projects')