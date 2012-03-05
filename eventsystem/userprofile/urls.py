from django.conf.urls.defaults import *

urlpatterns = patterns('eventsystem.userprofile.views',
    url(r'^profile/$', 'user_profile', name='user_profile'),
)
