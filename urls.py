from django.conf.urls.defaults import *
from django.contrib import databrowse

urlpatterns = patterns('',
    (r'^api/', include('sunlightapi.api.urls')),
    (r'^logs/', include('sunlightapi.logging.urls')),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^databrowse/(.*)', databrowse.site.root),
)
