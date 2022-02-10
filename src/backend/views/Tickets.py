from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Q
import requests

from backend.models.Ticket import Ticket
from backend.models.TicketComment import TicketComment
from backend.views.HelperFunctions import *

from backend.models.Project import Project

@login_required
def ticket_list_view(request): # ../tickets/
    tickets = Ticket.objects.filter(issuer = request.user).order_by('open')
    context = {
        'tickets': tickets,
        'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
    }
    return render(request, "tickets/ticket_list_template.html", context)

@login_required
def admin_ticket_list_view(request): # ../tickets/manage/
    if request.user.is_staff:
        tickets = Ticket.objects.filter(open=True)
        context = {
            'tickets': tickets,
            'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
        }
        return render(request, "tickets/admin_ticket_list_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't do this right now.")
        return redirect('/')

@login_required
def ticket_create_view(request): # ../tickets/create/
    if request.method == "POST":
        issuer = request.user
        projectPK = request.POST['project']
        project = Project.objects.get(pk=projectPK)
        content = request.POST['content']
        Ticket.objects.create(issuer=issuer, project=project, content=content)
        deleteMessages(request)
        messages.add_message(request, messages.SUCCESS, "A new ticket has been created.")
        return redirect('/tickets')
    else:
        projects = Project.objects.filter(Q(owner=request.user) | Q(mods=request.user) | Q(members=request.user))
        context = {
            'projects': projects,
            'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
        }
        return render(request, "tickets/ticket_create_template.html", context)

@login_required
def ticket_individual_view(request, ticketPK): # ../tickets/<int:ticketPK>/
    if isTicketIssuer(ticketPK, request.user) or request.user.is_staff:
        context = {
            'comments': TicketComment.objects.filter(ticket=Ticket.objects.get(pk=ticketPK)),
            'ticket': Ticket.objects.get(pk=ticketPK),
            'unreadNotifications': Notification.objects.filter(to=request.user, read=False),
        }
        return render(request, "tickets/ticket_individual_template.html", context)
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't view this ticket.")
        return redirect('/tickets')

@login_required
def ticket_comment_add_view(request, ticketPK): # ../tickets/<int:ticketPK>/comments/add/
    if (isTicketIssuer(ticketPK, request.user) or request.user.is_staff) and isOpen(ticketPK):
        if request.method == "POST":
            content = request.POST['content']
            ticket  = Ticket.objects.get(pk=ticketPK)
            TicketComment.objects.create(content=content, creator=request.user, ticket=ticket)
            deleteMessages(request)
            messages.add_message(request, messages.SUCCESS, "Comment added.")
        else:
            deleteMessages(request)
            messages.add_message(request, messages.ERROR, "Couldn't add comment to the ticket.")
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "Couldn't add comment to the ticket.")
    return redirect('/tickets/' + str(ticketPK))

@login_required
def ticket_comment_delete_view(request, ticketPK, commentPK): # ../tickets/<int:ticketPK>/comments/<int:commentPK>/delete/
    if isTicketCommentCreator(commentPK, request.user):
        TicketComment.objects.filter(pk=commentPK).delete()
        messages.add_message(request, messages.SUCCESS, "Comment has been deleted.")
        return redirect('/tickets/' + str(ticketPK))
    else:
        messages.add_message(request, messages.ERROR, "Could not delete comment.")
        return redirect('/tickets/' + str(ticketPK))

@login_required
def ticket_close_view(request, ticketPK): # ../tickets/<int:ticketPK>/close/
    if request.user.is_staff and ticketExists(ticketPK) and isOpen(ticketPK):
        Ticket.objects.filter(pk=ticketPK).update(open=False)
        deleteMessages(request)
        messages.add_message(request, messages.SUCCESS, "Ticket has been closed.")
        return redirect('/tickets/manage/')
    else:
        deleteMessages(request)
        messages.add_message(request, messages.ERROR, "You can't close this ticket.")
        return redirect('/tickets/manage/')