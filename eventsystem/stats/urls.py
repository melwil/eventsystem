from django.conf.urls.defaults import *

urlpatterns = patterns('eventsystem.stats.views',
    url(r'^$', 'stats_list', name='stats_list'),
)
