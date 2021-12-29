from django.contrib import messages

from backend.models.Comment import Comment
from backend.models.Project import Project
from backend.models.Task import Task

# Message functions
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

def isOwner(projectPK, givenUser): # check if the logged in user is owner of the project
    if projectExists(projectPK) and Project.objects.filter(pk=projectPK, owner=givenUser).exists():
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

def isCreator(commentPK, givenUser): # also checks if comment exists
    if Comment.objects.filter(pk=commentPK, creator=givenUser).exists():
        return True
    return False

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