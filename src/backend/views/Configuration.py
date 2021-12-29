from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from backend.views.HelperFunctions import *

@login_required
def settings_view(request):
    if request.method == "POST":
        darkmode = request.POST.get('darkmode', False)
        disableinformalmessages = request.POST.get('disableinformalmessages', False)
        if darkmode == "true":
            request.session['darkmode'] = True
        else:
            request.session['darkmode'] = False

        if disableinformalmessages == "true":
            request.session['disableinformalmessages'] = True
        else:
            request.session['disableinformalmessages'] = False
        return redirect('/settings')
    else:
        return render(request, 'configuration/settings_template.html')