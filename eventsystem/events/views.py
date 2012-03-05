# -*- encoding: utf8 -*-

from datetime import datetime

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
        if request.method == 'POST':
            ae = AttendanceEntry(user=request.user, event=event)
            ae.save()

    if request.user in event.attendees:
        context['status'] = 'attending'

    return render(request, 'events/details.html', {'event': event,})
