# -*- encoding: utf8 -*-

from datetime import datetime

from django.shortcuts import render, get_object_or_404

from eventsystem.events.models import Event

def list(request):
    events = Event.objects.filter(start_date__gte = datetime.now())

    return render(request, 'events/list.html', {'events': events,})

def details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    return render(request, 'events/details.html', {'event': event,})
