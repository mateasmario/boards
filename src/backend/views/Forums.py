from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import requests

from backend.models.Topic import Topic
from backend.models.TopicComment import TopicComment
from backend.views.HelperFunctions import *

from backend.models.Category import Category
from backend.models.Project import Project

@login_required
def forum_category_list_view(request, projectPK): # ../project/<projectPK>/forum/
    project = Project.objects.get(pk=projectPK)
    if hasForums(projectPK):
        if isMember(projectPK, request.user):
            context = {
                'project': project,
                'isOwner': isProjectOwner(projectPK, request.user),
                'isMod': isMod(projectPK, request.user),
                'categories': Category.objects.filter(project=project),
                'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
            }
            return render(request, "forums/forum_category_list_template.html", context)
        else:
            deleteMessages(request)
            messages.add_message(request, messages.ERROR, "You are not part of this project.")
            return redirect('/projects/')
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "This project doesn't have the Forums add-on enabled")
        return redirect('/projects/' + str(projectPK))

@login_required
def forum_category_create_view(request, projectPK): # ../project/<projectPK>/forum/category/create/
    if hasForums(projectPK) and isMod(projectPK, request.user):
        project = Project.objects.get(pk=projectPK)
        if request.method == "POST":
            title = request.POST['title']
            description = request.POST['description']
            if Category.objects.filter(title=title, project=project).exists():
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "A category with the same name already exists.")
                return redirect('/projects/' + str(projectPK) + '/forum')
            else:
                Category.objects.create(title=title, description=description, project=project)
                deleteMessages(request)
                messages.add_message(request, messages.SUCCESS, "Category has been successfully created.")
                return redirect('/projects/' + str(projectPK) + '/forum')
        else:
            context = {
                'project': project,
                'isOwner': isProjectOwner(projectPK, request.user),
                'isMod': isMod(projectPK, request.user),
                'categories': Category.objects.filter(project=project),
                'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
            }
            return render(request, "forums/forum_category_create_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You don't have the permission to create forum categories.")
        return redirect('/projects/' + str(projectPK))\

@login_required
def forum_category_update_view(request, projectPK, categoryPK): # ../project/<projectPK>/forum/category/<int:categoryPK>/edit
    if hasForums(projectPK) and isMod(projectPK, request.user) and categoryExists(categoryPK, projectPK):
        project = Project.objects.get(pk=projectPK)
        if request.method == "POST":
            title = request.POST['title']
            description = request.POST['description']
            if Category.objects.filter(title=title, project=project).exists() and title != Category.objects.get(pk=categoryPK).title:
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "A category with the same name already exists.")
                return redirect('/projects/' + str(projectPK) + '/forum')
            else:
                Category.objects.filter(pk=categoryPK).update(title=title, description=description, project=project)
                deleteMessages(request)
                messages.add_message(request, messages.SUCCESS, "Category has been successfully updated.")
                return redirect('/projects/' + str(projectPK) + '/forum/category/' + str(categoryPK))
        else:
            context = {
                'project': project,
                'isOwner': isProjectOwner(projectPK, request.user),
                'isMod': isMod(projectPK, request.user),
                'category': Category.objects.get(pk=categoryPK),
                'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
            }
            return render(request, "forums/forum_category_update_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't edit this category.")
        return redirect('/projects/' + str(projectPK))

@login_required
def forum_category_delete_view(request, projectPK, categoryPK): # ../project/<projectPK>/forum/category/<categoryPK>/delete/
    if categoryExists(categoryPK, projectPK) and isMod(projectPK, request.user):
        Category.objects.filter(pk=categoryPK).delete()
        deleteMessages(request)
        messages.add_message(request, messages.SUCCESS, "You successfully deleted the category.")
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't delete this category.")
    return redirect('/projects/' + str(projectPK) + '/forum')

@login_required
def forum_category_individual_view(request, projectPK, categoryPK): # ../project/<projectPK>/forum/category/<categoryPK>/
    if categoryExists(categoryPK, projectPK) and isMember(projectPK, request.user):
        project = Project.objects.get(pk=projectPK)
        category = Category.objects.get(pk=categoryPK)
        topics = Topic.objects.filter(category=category).order_by('pinned').reverse()
        context = {
            'project': project,
            'isOwner': isProjectOwner(projectPK, request.user),
            'isMod': isMod(projectPK, request.user),
            'category': category,
            'topics': topics,
            'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
        }
        return render(request, "forums/forum_category_individual_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't view this category.")
        return redirect('/projects/' + str(projectPK) + '/forum')

@login_required
def forum_topic_create_view(request, projectPK, categoryPK): # ../project/<projectPK>/forum/category/<categoryPK>/topic/create/
    if categoryExists(categoryPK, projectPK) and isMember(projectPK, request.user):
        project = Project.objects.get(pk=projectPK)
        category = Category.objects.get(pk=categoryPK, project=project)
        if request.method == "POST":
            title = request.POST['title']
            content = request.POST['content']
            Topic.objects.create(title=title, content=content, creator=request.user, category=category)
            messages.add_message(request, messages.SUCCESS, "Topic was created successfully.")
            return redirect('/projects/' + str(projectPK) + '/forum/category/' + str(categoryPK))
        else:
            context = {
                'project': project,
                'isOwner': isProjectOwner(projectPK, request.user),
                'isMod': isMod(projectPK, request.user),
                'category': Category.objects.get(pk=categoryPK),
                'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
            }
            return render(request, "forums/forum_topic_create_template.html", context)\

@login_required
def forum_topic_update_view(request, projectPK, categoryPK, topicPK): # ../project/<projectPK>/forum/category/<categoryPK>/topic/<int:topicPK>/update/
    if categoryExists(categoryPK, projectPK) and isMember(projectPK, request.user):
        project = Project.objects.get(pk=projectPK)
        category = Category.objects.get(pk=categoryPK, project=project)
        if request.method == "POST":
            title = request.POST['title']
            content = request.POST['content']
            Topic.objects.filter(pk=topicPK).update(title=title, content=content, creator=request.user, category=category)
            messages.add_message(request, messages.SUCCESS, "Topic was updated successfully.")
            return redirect('/projects/' + str(projectPK) + '/forum/category/' + str(categoryPK) + '/topic/' + str(topicPK))
        else:
            context = {
                'project': project,
                'isOwner': isProjectOwner(projectPK, request.user),
                'isMod': isMod(projectPK, request.user),
                'category': Category.objects.get(pk=categoryPK),
                'topic': Topic.objects.get(pk=topicPK),
                'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
            }
            return render(request, "forums/forum_topic_update_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't edit this topic.")
        return redirect('/projects/' + str(projectPK) + '/forum/category/' + str(categoryPK))

@login_required
def forum_topic_individual_view(request, projectPK, categoryPK, topicPK): # ../project/<projectPK>/forum/category/<categoryPK>/topic/<topicPK>/
    if categoryExists(categoryPK, projectPK) and topicExists(topicPK, categoryPK) and isMember(projectPK, request.user):
        if request.method == "POST":
            if categoryExists(categoryPK, projectPK) and topicExists(topicPK, categoryPK) and isMember(projectPK, request.user):
                if request.method == "POST":
                    content = request.POST['content']
                    topic = Topic.objects.get(pk=topicPK)
                    TopicComment.objects.create(content=content, creator=request.user, topic=topic)
                    deleteMessages(request)
                    messages.add_message(request, messages.SUCCESS, "Comment added.")
                else:
                    deleteMessages(request)
                    messages.add_message(request, messages.ERROR, "Couldn't add comment to the topic.")
            else:
                deleteMessages(request)
                messages.add_message(request, messages.ERROR, "Couldn't add comment to the topic.")
            return redirect('/projects/' + str(projectPK) + '/forum/category/' + str(categoryPK) + '/topic/' + str(topicPK))
        else:
            topic = Topic.objects.get(pk=topicPK)
            context = {
                'project': Project.objects.get(pk=projectPK),
                'category': Category.objects.get(pk=categoryPK),
                'isOwner': isProjectOwner(projectPK, request.user),
                'isMod': isMod(projectPK, request.user),
                'topic': topic,
                'comments': TopicComment.objects.filter(topic=topic),
                'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
            }
            return render(request, "forums/forum_topic_individual_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't view this topic.")
        return redirect('/projects/' + str(projectPK) + '/forum')

@login_required
def forum_topic_delete_view(request, projectPK, categoryPK, topicPK): # ../project/<projectPK>/forum/category/<categoryPK>/topic/<topicPK>/delete
    if categoryExists(categoryPK, projectPK) and topicExists(topicPK, categoryPK) and isTopicOwner(topicPK, request.user) and isMember(projectPK, request.user):
        Topic.objects.filter(pk=topicPK).delete()
        deleteMessages(request)
        messages.add_message(request, messages.SUCCESS, "You successfully deleted the topic.")
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't delete this topic.")
    return redirect('/projects/' + str(projectPK) + '/forum/category/' + str(categoryPK))

@login_required
def forum_topic_comment_delete_view(request, projectPK, categoryPK, topicPK, commentPK): # ../projects/<int:projectPK>/forums/category/<int:categoryPK>/topic/<int:topicPK>/comments/<int:commentPK>/delete
    if categoryExists(categoryPK, projectPK) and topicExists(topicPK, categoryPK) and isMember(projectPK, request.user) and isTopicCommentCreator(commentPK, request.user):
        TopicComment.objects.get(pk=commentPK).delete()
        messages.add_message(request, messages.SUCCESS, "Comment has been deleted.")
        return redirect('/projects/' + str(projectPK) + '/forum/category/' + str(categoryPK) + '/topic/' + str(topicPK))
    else:
        messages.add_message(request, messages.ERROR, "Could not delete comment.")
        return redirect('/projects/' + str(projectPK) + '/forum/category/' + str(categoryPK) + '/topic/' + str(topicPK))

@login_required
def forum_topic_pin_view(request, projectPK, categoryPK, topicPK): # ../projects/<int:projectPK>/forums/category/<int:categoryPK>/topic/<int:topicPK>/pin
    if categoryExists(categoryPK, projectPK) and topicExists(topicPK, categoryPK) and isMod(projectPK, request.user):
        Topic.objects.filter(pk=topicPK).update(pinned=True)
        deleteMessages(request)
        messages.add_message(request, messages.SUCCESS, "Topic was pinned.")
        return redirect('/projects/' + str(projectPK) + '/forum/category/' + str(categoryPK) + '/topic/' + str(topicPK))
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "Couldn't pin topic.")
        return redirect('/projects/' + str(projectPK) + '/forum/category/' + str(categoryPK) + '/topic/' + str(topicPK))

@login_required
def forum_topic_unpin_view(request, projectPK, categoryPK, topicPK): # ../projects/<int:projectPK>/forums/category/<int:categoryPK>/topic/<int:topicPK>/unpin
    if categoryExists(categoryPK, projectPK) and topicExists(topicPK, categoryPK) and isMod(projectPK, request.user):
        Topic.objects.filter(pk=topicPK).update(pinned=False)
        deleteMessages(request)
        messages.add_message(request, messages.SUCCESS, "Topic was unpinned.")
        return redirect('/projects/' + str(projectPK) + '/forum/category/' + str(categoryPK) + '/topic/' + str(topicPK))
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "Couldn't unpin topic.")
        return redirect('/projects/' + str(projectPK) + '/forum/category/' + str(categoryPK) + '/topic/' + str(topicPK))