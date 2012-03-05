
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from eventsystem.userprofile.models import UserProfile

@login_required()
def user_profile(request):
    events = request.user.get_profile().get_events()
    context = {}

    if len(events) > 0:
        context['events'] = events

    return render(request, 'user/profile.html', context)
