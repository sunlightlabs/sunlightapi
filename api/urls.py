from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *
from sunlightapi.api.models import Source

urlpatterns = patterns('sunlightapi.api.views',
                       
    # index
    url(r'^$', direct_to_template,
        {'template': 'index.html',
         'extra_context': { 'sources': Source.objects.all() }} ),

    # keys
    url(r'^register/$', 'register'),
    url(r'^confirmkey/(?P<apikey>[0-9a-f]{32})/$', 'confirm_registration'),
)
