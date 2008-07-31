from django.views.generic.list_detail import object_list
from django.conf.urls.defaults import *
from sunlightapi.logs.models import LogEntry

urlpatterns = patterns('sunlightapi.logs.views',

    # keys
    url(r'^register/$', 'register'),
    url(r'^confirmkey/(?P<apikey>[0-9a-f]{32})/$', 'confirm_registration'),

    # logs
    url(r'^logs/summary/$', 'summary'),
)
