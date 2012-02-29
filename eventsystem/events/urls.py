from django.conf.urls.defaults import *

urlpatterns = patterns('eventsystem.events.views',
    url(r'^$', 'list', name='list'),
    url(r'^(?P<event_id>\d+)/$', 'details', name='details'),
)
