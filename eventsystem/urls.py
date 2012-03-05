# -*- encoding: utf8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # Examples:
    (r'^$',             'eventsystem.events.views.list'),
    (r'^auth/',         include('eventsystem.auth.urls')),
    (r'^events/',       include('eventsystem.events.urls')),
    (r'^stats/',        include('eventsystem.stats.urls')),
    (r'^user/',         include('eventsystem.userprofile.urls')),
)
