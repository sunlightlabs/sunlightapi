from django.conf.urls.defaults import *
from django.contrib import databrowse

urlpatterns = patterns('',
    (r'^api/', include('sunlightapi.api.urls')),
    (r'^api/', include('sunlightapi.logs.urls')),
    (r'^api/admin/', include('django.contrib.admin.urls')),
    (r'^api/databrowse/(.*)', databrowse.site.root),
)
