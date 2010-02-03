from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template, redirect_to
from django.conf.urls.defaults import *

urlpatterns = patterns('sunlightapi.api.views',
    # index
    url(r'^$', direct_to_template, {'template': 'index.html', } ),
    url(r'^register/$', redirect_to, {'url': 'http://services.sunlightlabs.com/accounts/register/'}),
    url(r'^confirmkey/', direct_to_template, {'template': 'oldconfirm.html', } ),
)
