# -*- encoding: utf8 -*-

from datetime import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
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

    return render(request, 'events/details.html', context)

def attend(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if request.user.is_authenticated():
        if request.user not in event.attendees:
            if len(event.attendees) < event.seats:
                if allowed(request.user, event.restriction):
                    AttendanceEntry(user=request.user, event=event).save()
                    messages.success(request, "You were successfully added to this event.")
                else:
                    messages.error(request, "You do not meet the requirements for this event.")

    return HttpResponseRedirect(reverse(details, args=[event_id]))

def unattend(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if request.user.is_authenticated():
        if event.start_date <= datetime.now():
            messages.error(request, "You cannot unattend events after they have started.")
        else:
            ae = AttendanceEntry.objects.get(event=event, user=request.user)
            if ae:
                ae.delete()
                messages.success(request, "You were successfully removed from this event.")
        
    return HttpResponseRedirect(reverse(details, args=[event_id]))

def allowed(user, restriction):
    if restriction == 1:
        if user.get_profile().field_of_study <= 3:
            return True
    if restriction == 2:
        return True
    return False
