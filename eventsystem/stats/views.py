
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from eventsystem.events.models import Event

@login_required
def stats_home(request):
    if request.user.is_staff:
        events = Event.objects.all()

        return render(request, 'stats/home.html', {'events': events})
    else:
        messages.error(request, "You don't have access to this page.")
        return HttpResponseRedirect('/')

@login_required
def stats_users(request):
    if request.user.is_staff:
        users = User.objects.all().filter(userprofile__year__gte=1).order_by('first_name')

        return render(request, 'stats/users.html', {'users': users})
    else:
        messages.error(request, "You don't have access to this page.")
        return HttpResponseRedirect('/')

@login_required
def stats_event(request, event_id):
    if request.user.is_staff:
        event = get_object_or_404(Event, pk=event_id)
        
        return render(request, 'stats/event.html', {'event': event})
    else:
        messages.error(request, "You don't have access to this page.")
        return HttpResponseRedirect('/')
