from django.conf.urls.defaults import *
from django.contrib import databrowse

urlpatterns = patterns('',

    (r'^api/', include('api.urls')),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^databrowse/(.*)', databrowse.site.root),
)
