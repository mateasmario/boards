from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from backend.views.HelperFunctions import *

def auth_login_view(request): # ../auth/login/
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            deleteMessages(request)
            messages.add_message(request, messages.SUCCESS, "Successfully logged in as " + str(request.user) + ".")
            return redirect("/")
        else:
            messages.add_message(request, messages.ERROR, "Incorrect username and/or password.")
            return redirect("/auth/login")
    else:
        return render(request, "authentication/auth_login_template.html")

def auth_register_view(request): # ../auth/register/
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            confirmPassword = request.POST['confirmPassword']

            if User.objects.filter(email=email).exists():
                messages.add_message(request, messages.ERROR, "A user with the same e-mail already exists.")
                return redirect("/auth/register")
            elif User.objects.filter(username=username).exists():
                messages.add_message(request, messages.ERROR, "A user with the same username already exists.")
                return redirect("/auth/register")
            elif password != confirmPassword:
                messages.add_message(request, messages.ERROR, "The two passwords don't correspond.")
                return redirect("/auth/register")
            else:
                lenght = len(password)
                if hasDigit(password) and hasUpper(password) and hasLower(password) and lenght >= 8:
                    user = User.objects.create_user(email=email, username=username, password=password)
                    login(request, user)
                    return redirect("/")
                else:
                    messages.add_message(request, messages.ERROR, "Your password should have a length of at least 8 characters, contain at least a digit, contain at least an uppercase letter and contain at least a lowercase letter.")
                    return redirect("/auth/register")
        else:
            return render(request, "authentication/auth_register_template.html")

@login_required
def auth_logout_view(request): # ../auth/logout
    logout(request)
    return redirect('/')