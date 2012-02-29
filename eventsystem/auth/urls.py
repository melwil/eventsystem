# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('eventsystem.auth.views',
       (r'^$', 'login'),
       url(r'^login/$', 'login', name='auth_login'),
       url(r'^logout/$', 'logout', name='auth_logout'),
       url(r'^register/$', 'register', name='auth_register'),
)
