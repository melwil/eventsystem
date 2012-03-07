from django.conf.urls.defaults import *

urlpatterns = patterns('eventsystem.stats.views',
    url(r'^$', 'stats_home', name='stats_home'),
    url(r'^users/$', 'stats_users', name='stats_users'),
    url(r'^event/(?P<event_id>\d+)/$', 'stats_event', name='stats_event'),
)
