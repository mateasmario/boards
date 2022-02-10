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
from backend.views.Forums import *
from backend.views.Profile import *
from backend.views.Projects import *
from backend.views.Tasks import *
from backend.views.Configuration import *
from backend.views.Tickets import *
from backend.views.Notifications import *

urlpatterns = [
    # General
    path('admin/', admin.site.urls),
    path('', index_view, name="index_view"),

    # Authentication
    path('auth/login/', auth_login_view, name="auth_login_view"),
    path('auth/register/', auth_register_view, name="auth_register_view"),
    path('auth/logout/', auth_logout_view, name="auth_logout_view"),
    path('auth/changepassword/', auth_changepassword_view, name="auth_changepassword_view"),

    # Projects
    path('projects/', project_list_view, name="project_list_view"),
    path('projects/<int:projectPK>/', project_individual_view, name="project_individual_view"),
    path('projects/create/', project_create_view, name="project_create_view"),
    path('projects/<int:projectPK>/update/', project_update_view, name='project_update_view'),
    path('projects/<int:projectPK>/delete/', project_delete_view, name="project_delete_view"),
    path('projects/<int:projectPK>/invite/', project_invite_view),
    path('projects/<int:projectPK>/members/', project_members_view, name="project_members_view"),
    path('projects/<int:projectPK>/github', project_github_view, name="project_github_view"),
    path('projects/<int:projectPK>/promote/<str:username>', project_promote_view, name="project_promote_view"),
    path('projects/<int:projectPK>/demote/<str:username>', project_demote_view, name="project_demote_view"),
    path('projects/<int:projectPK>/kick/<str:username>', project_kick_view, name="project_kick_view"),

    # Tasks
    path('projects/<int:projectPK>/tasks/', task_list_view, name="task_list_view"),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/', task_individual_view, name="task_individual_view"),
    path('projects/<int:projectPK>/tasks/create/', task_create_view, name="task_create_view"),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/update/', task_update_view, name="task_update_view"),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/delete/', task_delete_view, name="task_delete_view"),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/mark_solved/', task_mark_solved_view, name="task_mark_solved_view"),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/mark_unsolved/', task_mark_unsolved_view, name="task_mark_unsolved_view"),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/comments/add/', task_comment_add_view, name="task_comment_add_view"),
    path('projects/<int:projectPK>/tasks/<int:taskPK>/comments/<int:commentPK>/delete/', task_comment_delete_view, name="task_comment_delete_view"),
    path('projects/<int:projectPK>/leave/', project_leave_view, name="project_leave_view"),

    # Add-ons
    path('projects/<int:projectPK>/addons/', project_addon_view, name="project_addon_view"),

    # Forums
    path('projects/<int:projectPK>/forum/', forum_category_list_view, name="forum_category_list_view"),
    path('projects/<int:projectPK>/forum/category/create/', forum_category_create_view, name="forum_category_create_view"),
    path('projects/<int:projectPK>/forum/category/<int:categoryPK>/delete/', forum_category_delete_view, name="forum_category_delete_view"),
    path('projects/<int:projectPK>/forum/category/<int:categoryPK>/', forum_category_individual_view, name="forum_category_individual_view"),
    path('projects/<int:projectPK>/forum/category/<int:categoryPK>/update/', forum_category_update_view, name="forum_category_update_view"),
    path('projects/<int:projectPK>/forum/category/<int:categoryPK>/topic/create/', forum_topic_create_view, name="forum_topic_create_view"),
    path('projects/<int:projectPK>/forum/category/<int:categoryPK>/topic/<int:topicPK>/', forum_topic_individual_view, name="forum_topic_individual_view"),
    path('projects/<int:projectPK>/forum/category/<int:categoryPK>/topic/<int:topicPK>/update/', forum_topic_update_view, name="forum_topic_update_view"),
    path('projects/<int:projectPK>/forum/category/<int:categoryPK>/topic/<int:topicPK>/delete/', forum_topic_delete_view, name="forum_topic_delete_view"),
    path('projects/<int:projectPK>/forum/category/<int:categoryPK>/topic/<int:topicPK>/comments/<int:commentPK>/delete/', forum_topic_comment_delete_view, name="forum_topic_comment_delete_view"),
    path('projects/<int:projectPK>/forum/category/<int:categoryPK>/topic/<int:topicPK>/pin/', forum_topic_pin_view, name="forum_topic_pin_view"),
    path('projects/<int:projectPK>/forum/category/<int:categoryPK>/topic/<int:topicPK>/unpin/', forum_topic_unpin_view, name="forum_topic_unpin_view"),

    # Tickets
    path('tickets/', ticket_list_view, name="ticket_list_view"),
    path('tickets/create/', ticket_create_view, name="ticket_create_view"),
    path('tickets/<int:ticketPK>/', ticket_individual_view, name="ticket_individual_view"),
    path('tickets/<int:ticketPK>/comments/add/', ticket_comment_add_view, name="ticket_comment_add_view"),
    path('tickets/<int:ticketPK>/comments/<int:commentPK>/delete', ticket_comment_delete_view, name="ticket_comment_delete_view"),
    path('tickets/manage/', admin_ticket_list_view, name="admin_ticket_list_view"),
    path('tickets/<int:ticketPK>/close/', ticket_close_view, name="ticket_close_view"),

    # Profile
    path('profile/<str:username>/', profile_view, name="profile_view"),

    # Configuration
    path('settings/', settings_view, name="settings_view"),

    # Notifications
    path('notifications/', notification_list_view, name="notification_list_view"),
    path('notifications/<int:notificationPK>/', notification_individual_view, name="notification_individual_view"),
    path('notifications/<int:notificationPK>/delete/', notification_delete_view, name="notification_delete_view"),
    path('notifications/<int:notificationPK>/accept/', notification_accept_view, name="notification_accept_view"),
]
