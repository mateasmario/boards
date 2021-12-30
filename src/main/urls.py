"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from backend.views.Authentication import *
from backend.views.Profile import *
from backend.views.Projects import *
from backend.views.Tasks import *
from backend.views.Configuration import *

urlpatterns = [
    # General
    path('admin/', admin.site.urls),
    path('', index_view, name="index_view"),

    # Authentication
    path('auth/login/', auth_login_view, name="auth_login_view"),
    path('auth/register/', auth_register_view, name="auth_register_view"),
    path('auth/logout/', auth_logout_view, name="auth_logout_view"),

    # Projects
    path('projects/', project_list_view, name="project_list_view"),
    path('projects/<int:projectPK>/', project_individual_view, name="project_individual_view"),
    path('projects/create/', project_create_view, name="project_create_view"),
    path('projects/<int:projectPK>/update/', project_update_view, name='project_update_view'),
    path('projects/<int:projectPK>/delete/', project_delete_view, name="project_delete_view"),
    path('projects/<int:projectPK>/invite/', project_invite_view),
    path('projects/<int:projectPK>/members/', project_members_view, name="project_members_view"),
    path('projects/<int:projectPK>/github', project_github_view, name="project_github_view"),

    # Tasks
    path('projects/<int:projectPK>/tasks/', task_list_view, name="task_list_view"),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/', task_individual_view, name="task_individual_view"),
    path('projects/<int:projectPK>/tasks/create/', task_create_view, name="task_create_view"),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/delete/', task_delete_view, name="task_delete_view"),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/mark_solved/', task_mark_solved_view, name="task_mark_solved_view"),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/mark_unsolved/', task_mark_unsolved_view, name="task_mark_unsolved_view"),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/comments/add', task_comment_add_view, name="task_comment_add_view"),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/comments/<int:commentPK>/delete', task_comment_delete_view, name="task_comment_delete_view"),

    # Profile
    path('profile/<str:username>/', profile_view, name="profile_view"),

    # Configuration
    path('settings/', settings_view, name="settings_view"),
]
