import random

import requests
from django.contrib import messages

from backend.models.Category import Category
from backend.models.Notification import Notification
from backend.models.TaskComment import TaskComment
from backend.models.Project import Project
from backend.models.Task import Task

# Message functions
from backend.models.Ticket import Ticket
from backend.models.TicketComment import TicketComment
from backend.models.Topic import Topic
from backend.models.TopicComment import TopicComment


def deleteMessages(request):
    system_messages = messages.get_messages(request)
    for message in system_messages:
        pass

# String functions
def hasDigit(string):
    for char in string:
        if char.isdigit():
            return True
    return False

def hasUpper(string):
    for char in string:
        if char.isupper():
            return True
    return False

def hasLower(string):
    for char in string:
        if char.islower():
            return True
    return False

# User functions
def UserExists(username): # check if user exists in the database
    if User.objects.filter(username=username).exists():
        return True
    return False

# Project functions
def projectExists(projectPK): # check if project exists in the database
    if Project.objects.filter(pk=projectPK).exists():
        return True
    return False

def isProjectOwner(projectPK, givenUser): # check if the logged in user is owner of the project
    if Project.objects.filter(pk=projectPK, owner=givenUser).exists():
        return True
    return False

def isMod(projectPK, givenUser): # check if the logged in user is at least a mod of the project
    if projectExists(projectPK):
        if Project.objects.filter(pk=projectPK, mods=givenUser).exists() or Project.objects.filter(pk=projectPK, owner=givenUser).exists():
            return True
    return False

def isMember(projectPK, givenUser): # check if the logged in user is at least a member of the project
    if projectExists(projectPK):
        if Project.objects.filter(pk=projectPK, owner=givenUser).exists() or Project.objects.filter(pk=projectPK, mods=givenUser).exists() or Project.objects.filter(pk=projectPK, members=givenUser).exists():
            return True
    return False

def isIssuer(taskPK, givenUser):
    if taskExists(taskPK):
        if Task.objects.filter(pk=taskPK, issuer=givenUser).exists():
            return True
        return False

# Task functions
def taskExists(taskPK):
    if Task.objects.filter(pk=taskPK).exists():
        return True
    return False

def taskBelongsToProject(taskPK, projectPK):
    if projectExists(projectPK):
        project = Project.objects.get(pk=projectPK)
        if Task.objects.filter(pk=taskPK, project=project).exists():
            return True
    return False

def isAssignee(taskPK, givenUser):
    if taskExists(taskPK) and Task.objects.filter(pk=taskPK, assignee=givenUser).exists():
        return True
    return False

def isTaskCommentCreator(commentPK, givenUser): # also checks if comment exists
    if TaskComment.objects.filter(pk=commentPK, creator=givenUser).exists():
        return True
    return False

def isTopicCommentCreator(commentPK, givenUser): # also checks if comment exists
    if TopicComment.objects.filter(pk=commentPK, creator=givenUser).exists():
        return True
    return False

# GitHub functions
def isGitHubURL(url):
    url = url.lower()
    formattedURL = url.split(".")
    print(formattedURL)
    try:
        # for http://github.com and https://github.com
        if ((formattedURL[0] == "http://github" or formattedURL[0] == "https://github") and formattedURL[1][0:3] == "com" and not formattedURL[1][3].isalpha()):
            return True
        # for http://www.github.com and https://www.github.com
        elif ((formattedURL[0] == "http://www" or formattedURL[0] == "https://www") and formattedURL[1] == "github" and formattedURL[2][0:3] == "com" and not formattedURL[2][3].isalpha()):
            return True
        # for www.github.com
        elif (formattedURL[0] == "www" and formattedURL[1] == "github" and formattedURL[2][0:3] == "com" and not formattedURL[2][3].isalpha()):
            return True
        # for github.com
        elif (formattedURL[0] == "github" and formattedURL[1][0:3] == "com" and not formattedURL[1][3].isalpha()):
            return True
    except:
        return False
    return False

def repoExists(githubURL):
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    urlList = githubURL.split("/")
    url = ""
    url += urlList[-2]
    url += "/"
    url += urlList[-1]
    response = requests.get('https://api.github.com/repos/' + url,
                            auth=('mateasmario', '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'), headers=headers)
    github = response.json()
    try:
        message = github['message']
    except:
        message = "Found"
    if message == "Not Found":
        return False
    return True

# Forums functions
def hasForums(projectPK):
    project = Project.objects.get(pk=projectPK)
    if project.forums:
        return True
    return False

def categoryExists(categoryPK, projectPK):
    if hasForums(projectPK) and projectExists(projectPK):
        project = Project.objects.get(pk=projectPK)
        if Category.objects.filter(pk=categoryPK, project=project).exists():
            return True
    return False

def topicExists(topicPK, categoryPK):
    if Category.objects.filter(pk=categoryPK).exists():
        category = Category.objects.get(pk=categoryPK)
        if Topic.objects.filter(pk=topicPK, category=category):
            return True
    return False

def isTopicOwner(topicPK, givenUser):
    if Topic.objects.filter(pk=topicPK, creator=givenUser).exists():
        return True
    return False

# Security functions
def generateQuestion():
    operatorPosition = random.randint(0, 1) # 0 for "+", 1 for "-"

    if operatorPosition == 0:
        first = random.randint(1, 100)
        second = random.randint(1, 100)
        operator = "+"
        answer = first + second
    else:
        first = random.randint(1, 100)
        second = first
        while second >= first:
            second = random.randint(1, 100)
        operator = "-"
        answer = first-second
    return [operator, first, second, answer]

# Ticket functions
def ticketExists(ticketPK):
    if Ticket.objects.filter(pk=ticketPK).exists():
        return True
    return False

def isTicketIssuer(ticketPK, givenUser):
    if Ticket.objects.filter(pk=ticketPK, issuer=givenUser).exists():
        return True
    return False

def isTicketCommentCreator(commentPK, givenUser): # also checks if comment exists
    if TicketComment.objects.filter(pk=commentPK, creator=givenUser).exists():
        return True
    return False

def isOpen(ticketPK):
    if Ticket.objects.filter(pk=ticketPK, open=True).exists():
        return True
    return False

def notificationAssignedTo(notificationPK, givenUser):
    if Notification.objects.filter(pk=notificationPK, to=givenUser).exists():
        return True
    return False