from django.conf.urls.defaults import *

urlpatterns = patterns('eventsystem.events.views',
    url(r'^$', 'list', name='list'),
    url(r'^(?P<event_id>\d+)/$', 'details', name='details'),
    url(r'^(?P<event_id>\d+)/attend/$', 'attend', name='attend'),
    url(r'^(?P<event_id>\d+)/unattend/$', 'unattend', name='unattend'),
)
