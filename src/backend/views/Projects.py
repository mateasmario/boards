from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import requests

from backend.models.Category import Category
from backend.models.Project import Project

from backend.views.HelperFunctions import *

def index_view(request): # ../
    return redirect('/projects')

@login_required
def support_view(request):
    return render(request, "support_template.html")

@login_required
def project_list_view(request): # ../projects/
    ownedProjects = Project.objects.filter(owner=request.user)
    moderatingProjects = Project.objects.filter(mods=request.user)
    workingOnProjects = Project.objects.filter(members=request.user)

    if ownedProjects.count() == 0 and moderatingProjects.count() == 0 and workingOnProjects.count() == 0:
        hasProjects = False
    else:
        hasProjects = True

    context = {
        'ownedProjects': ownedProjects,
        'moderatingProjects': moderatingProjects,
        'workingOnProjects': workingOnProjects,
        'hasProjects': hasProjects,
        'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
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
            'isOwner': isProjectOwner(projectPK, request.user),
            'isMod': isMod(projectPK, request.user),
            'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
            'solvedTasks': Task.objects.filter(project=project, solved=True),
            'totalTasks': Task.objects.filter(project=project),
            'openTickets': Ticket.objects.filter(project=project, open=True),
            'invitationsWithoutReply': Notification.objects.filter(type='PI', project=project),
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
            elif github != "" and repoExists(github) == False:
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "The repo with the specified URL does not exist.")
                return redirect("/projects/create")
            else:
                if github[0:4] != "http" and github != "":
                    githubNew = "https://" + github
                    github = githubNew
                Project.objects.create(title=title, description=description, averageNoPeople=averageNoPeople, github=github, devwebsite=devwebsite, owner=owner)
                deleteMessages(request)
                messages.add_message(request, messages.SUCCESS, "Project '" + title + "' was created.")
                return redirect("/projects")
    else:
        return render(request, "projects/project_create_template.html")

@login_required # ../projects/<int:pk>/update/
def project_update_view(request, projectPK):
    if isProjectOwner(projectPK, request.user) == True:
        if request.method == "POST":
            title = request.POST['title']
            description = request.POST['description']
            averageNoPeople = request.POST['averageNoPeople']
            github = request.POST['github']
            devwebsite = request.POST['devwebsite']

            if Project.objects.filter(title=title, owner=Project.objects.get(pk=projectPK).owner).exists() and title != Project.objects.get(pk=projectPK).title:
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "Project with the same name already exists in your account.")
                return redirect("/projects/" + str(projectPK) + "/update")

            if github != "" and isGitHubURL(github) == False:
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "The URL you typed in is not a valid GitHub repo link.")
                return redirect("/projects/" + str(projectPK) + "/update")
            elif github != "" and repoExists(github) == False:
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "The repo with the specified URL does not exist.")
                return redirect("/projects/" + str(projectPK) + "/update")
            else:
                if github[0:4] != "http" and github != "":
                    githubNew = "https://" + github
                    github = githubNew
                Project.objects.filter(pk=projectPK).update(title=title, description=description, averageNoPeople=averageNoPeople, devwebsite=devwebsite, github=github)
                deleteMessages(request)
                messages.add_message(request, messages.SUCCESS, "Project '" + title + "' has been updated.")
                return redirect('/projects/' + str(projectPK))
        else:
            project = Project.objects.get(pk=projectPK)
            context = {
                'project': project,
                'isOwner': isProjectOwner(projectPK, request.user),
                'isMod': isMod(projectPK, request.user),
                'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
            }
            return render(request, "projects/project_update_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't edit that project.")
        return redirect('/projects')

@login_required # ../projects/<int:projectPK>/delete/
def project_delete_view(request, projectPK):
    if isProjectOwner(projectPK, request.user) == True:
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
            # project.members.add(user)
            if Notification.objects.filter(type="PI", to=User.objects.get(username=username), project=project).exists():
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "User has been already invited to the project.")
                return redirect('/projects/' + str(projectPK))
            else:
                Notification.objects.create(type="PI", to=User.objects.get(username=username), project=project)
                messages.add_message(request, messages.INFO, "User has been invited to the project.")
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
            'isOwner': isProjectOwner(projectPK, request.user),
            'isMod': isMod(projectPK, request.user),
            'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
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
                'isOwner': isProjectOwner(projectPK, request.user),
                'isMod': isMod(projectPK, request.user),
                'github': github,
                'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
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

@login_required
def project_addon_view(request, projectPK): # ../projects/<int:projectPK>/addons
    if isProjectOwner(projectPK, request.user):
        if request.method == "POST":
            forums = request.POST.get('forums', False)
            contact_page = request.POST.get('contact_page', False)
            resources = request.POST.get('resources', False)
            faq = request.POST.get('faq', False)
            schema = request.POST.get('schema', False)
            meetings = request.POST.get('meetings', False)
            discussions = request.POST.get('discussions', False)

            if forums == "true":
                Project.objects.filter(pk=projectPK).update(forums=True)
            else:
                Project.objects.filter(pk=projectPK).update(forums=False)

            if contact_page == "true":
                Project.objects.filter(pk=projectPK).update(contact_page=True)
            else:
                Project.objects.filter(pk=projectPK).update(contact_page=False)

            if resources == "true":
                Project.objects.filter(pk=projectPK).update(resources=True)
            else:
                Project.objects.filter(pk=projectPK).update(resources=False)

            if faq == "true":
                Project.objects.filter(pk=projectPK).update(faq=True)
            else:
                Project.objects.filter(pk=projectPK).update(faq=False)

            if schema == "true":
                Project.objects.filter(pk=projectPK).update(schema=True)
            else:
                Project.objects.filter(pk=projectPK).update(schema=False)

            if meetings == "true":
                Project.objects.filter(pk=projectPK).update(meetings=True)
            else:
                Project.objects.filter(pk=projectPK).update(meetings=False)

            if discussions == "true":
                Project.objects.filter(pk=projectPK).update(discussions=True)
            else:
                Project.objects.filter(pk=projectPK).update(discussions=False)

            deleteMessages(request)
            messages.add_message(request, messages.SUCCESS, "Changes saved.")
            return redirect('/projects/' + str(projectPK) + "/addons")
        else:
            project = Project.objects.get(pk=projectPK)
            context = {
                'project': project,
                'isOwner': isProjectOwner(projectPK, request.user),
                'isMod': isMod(projectPK, request.user),
                'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
            }
            return render(request, "projects/project_addon_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You don't have the permission to do this.")
        return redirect('/projects/' + str(projectPK))

@login_required
def project_leave_view(request, projectPK): # ../projects/<int:projectPK>/leave/
    if isMember(projectPK, request.user) and not isProjectOwner(projectPK, request.user):
        project = Project.objects.get(pk=projectPK)
        project.members.remove(request.user)
        deleteMessages(request)
        messages.add_message(request, messages.SUCCESS, "You left the project.")
        return redirect('/projects/')
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't leave this project.")
        return redirect('/projects/' + str(projectPK))

@login_required
def project_promote_view(request, projectPK, username): # ../projects/<int:projectPK>/promote/<str:username>/
    if not isProjectOwner(projectPK, request.user):
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't promote or demote members.")
        return redirect('/projects/' + str(projectPK) + '/members/')
    else:
        if isMember(projectPK, User.objects.get(username=username)):
            member = User.objects.get(username=username)
            if isMod(projectPK, member):
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "The user is already a moderator.")
                return redirect('/projects/' + str(projectPK) + '/members/')
            else:
                project = Project.objects.get(pk=projectPK)
                project.mods.add(member)
                project.members.remove(member)
                deleteMessages(request)
                messages.add_message(request, messages.SUCCESS, "User is now a moderator.")
                return redirect('/projects/' + str(projectPK) + '/members/')
        else:
            deleteMessages(request)
            messages.add_message(request, messages.ERROR, "User is not part of the project.")
            return redirect('/projects/' + str(projectPK) + '/members/')

@login_required
def project_demote_view(request, projectPK, username): # ../projects/<int:projectPK>/promote/<str:username>/
    if not isProjectOwner(projectPK, request.user):
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't promote or demote members.")
        return redirect('/projects/' + str(projectPK) + '/members/')
    else:
        if isMember(projectPK, User.objects.get(username=username)):
            member = User.objects.get(username=username)
            if not isMod(projectPK, member):
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "The user is not a moderator.")
                return redirect('/projects/' + str(projectPK) + '/members/')
            else:
                project = Project.objects.get(pk=projectPK)
                project.members.add(member)
                project.mods.remove(member)
                deleteMessages(request)
                messages.add_message(request, messages.SUCCESS, "User is now a member.")
                return redirect('/projects/' + str(projectPK) + '/members/')
        else:
            deleteMessages(request)
            messages.add_message(request, messages.ERROR, "User is not part of the project.")
            return redirect('/projects/' + str(projectPK) + '/members/')

@login_required
def project_kick_view(request, projectPK, username): # ../projects/<int:projectPK>/kick/<str:username>
    if isMember(projectPK, User.objects.get(username=username)):
        project = Project.objects.get(pk=projectPK)
        member = User.objects.get(username=username)
        if isOwner(projectPK, request.user):
            project.members.remove(member)
            project.mods.remove(member)
            deleteMessages(request)
            messages.add_message(request, messages.SUCCESS, "User is no longer part of the project.")
            return redirect('/projects/' + str(projectPK) + '/members/')
        else:
            if isMod(projectPK, request.user):
                if not isMod(projectPK, member):
                    project.members.remove(member)
                    project.mods.remove(member)
                    deleteMessages(request)
                    messages.add_message(request, messages.SUCCESS, "User is no longer part of the project.")
                    return redirect('/projects/' + str(projectPK) + '/members/')
                else:
                    deleteMessages(request)
                    messages.add_message(request, messages.ERROR, "You can't kick a member with a rank equal or higher than yours.")
                    return redirect('/projects/' + str(projectPK) + '/members/')
            else:
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "You must be a moderator in order to kick users.")
                return redirect('/projects/' + str(projectPK) + '/members/')
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "User is not part of the project.")
        return redirect('/projects/' + str(projectPK) + '/members/')