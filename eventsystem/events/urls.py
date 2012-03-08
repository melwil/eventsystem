from django.conf.urls.defaults import *

from eventsystem.events.pdfgenerator import pdf

urlpatterns = patterns('eventsystem.events.views',
    url(r'^$', 'list', name='list'),
    url(r'^(?P<event_id>\d+)/$', 'details', name='details'),
    url(r'^(?P<event_id>\d+)/attend/$', 'attend', name='attend'),
    url(r'^(?P<event_id>\d+)/unattend/$', 'unattend', name='unattend'),
    url(r'^(?P<event_id>\d+)/attendees/$', pdf, name='event_attendees'),
    url(r'^(?P<event_id>\d+)/attendee_emails/$', 'attendee_emails', name='attendee_emails'),
)
