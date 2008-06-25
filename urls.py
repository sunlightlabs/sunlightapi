from django.conf.urls.defaults import *
from django.contrib import databrowse

urlpatterns = patterns('',
    (r'^api/api/', include('sunlightapi.api.urls')),
    (r'^api/logs/', include('sunlightapi.logs.urls')),
    (r'^api/admin/', include('django.contrib.admin.urls')),
    (r'^api/databrowse/(.*)', databrowse.site.root),
)
