
from django.contrib import admin

from eventsystem.events.models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'location', 'seats']

admin.site.register(Event, EventAdmin)
