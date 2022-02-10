from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from backend.views.HelperFunctions import *

@login_required
def profile_view(request, username):
    if User.objects.filter(username=username).exists():
        tasksSolved = Task.objects.filter(solved=True, assignee=request.user).count()
        context = {
            'profile': User.objects.get(username=username),
            'tasksSolved': tasksSolved,
            'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
        }
        return render(request, "profile/profile_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "The user you're looking for does not exist.")
        return redirect('/profile/' + str(request.user))