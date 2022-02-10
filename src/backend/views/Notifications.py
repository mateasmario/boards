from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from backend.models.Notification import Notification
from backend.views.HelperFunctions import *

@login_required
def notification_list_view(request): # ../notifications/
    notifications = Notification.objects.filter(to=request.user).order_by('date').reverse()
    if notifications.exists():
        hasNotifications = True
    else:
        hasNotifications = False
    context = {
        "notifications": notifications,
        'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
        'hasNotifications': hasNotifications,
    }
    return render(request, "notifications/notification_list_template.html", context)

@login_required
def notification_individual_view(request, notificationPK): # ../notifications/<int:notificationPK>/
    if notificationAssignedTo(notificationPK, request.user):
        notification = Notification.objects.get(pk=notificationPK)
        if notification.read == False:
            Notification.objects.filter(pk=notificationPK).update(read=True)
        context = {
            'notification': notification,
            'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
        }
        return render(request, "notifications/notification_individual_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't view this notification.")
        return redirect('/notifications/')

@login_required
def notification_delete_view(request, notificationPK): # ../notifications/<int:notificationPK>/delete/
    if notificationAssignedTo(notificationPK, request.user):
        Notification.objects.filter(pk=notificationPK).delete()
        deleteMessages(request)
        messages.add_message(request, messages.SUCCESS, "You have deleted the notification.")
        return redirect('/notifications/')
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't delete this notification.")
        return redirect('/notifications/')

@login_required
def notification_accept_view(request, notificationPK): # ../notifications/<int:notificationPK>/delete/
    if notificationAssignedTo(notificationPK, request.user) and Notification.objects.get(pk=notificationPK).type == "PI":
        notification = Notification.objects.get(pk=notificationPK)
        project = Project.objects.get(pk=notification.project.pk)
        project.members.add(request.user)
        Notification.objects.filter(pk=notificationPK).delete()
        deleteMessages(request)
        messages.add_message(request, messages.SUCCESS, "You have accepted the invitation.")
        return redirect('/notifications/')
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't accept this invitation.")
        return redirect('/notifications/')