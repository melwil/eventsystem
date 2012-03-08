# -*- encoding: utf8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

from eventsystem.events.models import Event, AttendanceEntry

def list(request):
    events = Event.objects.filter(start_date__gte = datetime.now())

    return render(request, 'events/list.html', {'events': events,})

def details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    context = {}
    context['event'] = event

    if request.user.is_authenticated():
        attendees = event.attendees
        if request.user in attendees:
            context['status'] = 'attending'
        else:
            if len(attendees) >= event.seats:
                context['status'] = 'nofree'
    else:
        context['status'] = 'needlogin'

    return render(request, 'events/details.html', context)

@login_required
def attend(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if request.user.is_authenticated():
        if request.user not in event.attendees:
            if len(event.attendees) < event.seats:
                profile = request.user.get_profile()
                if event.title == 'Middag' and not profile.can_attend_dinner():
                    messages.error(request, "You need to attend as least 2 events in order to sign up for the dinner.")
                else:
                    if _allowed(request.user, event.restriction):
                        AttendanceEntry(user=request.user, event=event).save()
                        messages.success(request, "You were successfully added to this event.")
                    else:
                        messages.error(request, "You do not meet the requirements for this event.")

    return HttpResponseRedirect(reverse(details, args=[event_id]))

@login_required
def unattend(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if request.user.is_authenticated():
        if event.start_date <= datetime.now():
            messages.error(request, "You cannot unattend events after they have started.")
        else:
            profile = request.user.get_profile()
            if profile.is_attending_dinner() and len(profile.get_events()) <= 3 and event.title != 'Middag':
                messages.error(request, "You can't attend less than 2 events when you are signed up for the dinner. Unattend the dinner first.")
            else:
                ae = AttendanceEntry.objects.get(event=event, user=request.user)
                if ae:
                    ae.delete()
                    messages.success(request, "You were successfully removed from this event.")
        
    return HttpResponseRedirect(reverse(details, args=[event_id]))

def _allowed(user, restriction):
    if restriction == 1:
        if user.get_profile().field_of_study <= 3:
            return True
    if restriction == 2:
        return True
    return False

@login_required()
def attendee_emails(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    userlist = ""
    for attendee in event.attendees:
        userlist += attendee.email + ", "

    return HttpResponse(userlist)
