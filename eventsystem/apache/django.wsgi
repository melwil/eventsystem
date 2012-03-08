#
# mod_wsgi handler for the onlineweb django project
#

import site
site.addsitedir('/usr/local/virtualenv/melwil.net/lib/python2.6/site-packages')

import os
import sys

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

sys.path.append('/home/ha/havardsv/web/other/eventsystem/')
sys.path.append('/home/ha/havardsv/web/other/eventsystem/eventsystem/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'eventsystem.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
