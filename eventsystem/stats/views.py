
from django.contrib.auth.models import User
from django.shortcuts import render

def stats_list(request):
    users = User.objects.all().filter(userprofile__year__gte=1).order_by('first_name')

    return render(request, 'stats/users.html', {'users': users})
