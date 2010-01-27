from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *

urlpatterns = patterns('sunlightapi.api.views',
    # index
    url(r'^$', direct_to_template, {'template': 'index.html', } ),
)
