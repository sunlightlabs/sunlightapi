from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template, redirect_to
from django.conf.urls.defaults import *

urlpatterns = patterns('sunlightapi.api.views',
    url(r'^$', redirect_to, {'url': 'http://services.sunlightlabs.com/docs/Sunlight_Congress_API/'}),
    url(r'^register/$', redirect_to, {'url': 'http://services.sunlightlabs.com/accounts/register/'}),
)
