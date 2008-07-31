from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib import databrowse

admin.autodiscover()

urlpatterns = patterns('',
    (r'^api/', include('sunlightapi.api.urls')),
    (r'^api/', include('sunlightapi.logs.urls')),
    (r'^api/admin/(.*)', admin.site.root),
    (r'^api/databrowse/(.*)', databrowse.site.root),
)
