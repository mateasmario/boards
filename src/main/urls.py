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
from backend.views.Projects import *
from backend.views.Tasks import *

urlpatterns = [
    # General
    path('admin/', admin.site.urls),
    path('', index_view),

    # Authentication
    path('auth/login/', auth_login_view),
    path('auth/register/', auth_register_view),
    path('auth/logout/', auth_logout_view),

    # Projects
    path('projects/', project_list_view),
    path('projects/<int:projectPK>/', project_individual_view, name="project_individual_view"),
    path('projects/create/', project_create_view),
    path('projects/<int:projectPK>/update/', project_update_view),
    path('projects/<int:projectPK>/delete/', project_delete_view),

    # Tasks
    path('projects/<int:projectPK>/tasks/', task_list_view),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/', task_individual_view, name="task_individual_view"),
    path('projects/<int:projectPK>/tasks/create/', task_create_view),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/delete/', task_delete_view),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/mark_solved/', task_mark_solved_view),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/mark_unsolved/', task_mark_unsolved_view),
]
