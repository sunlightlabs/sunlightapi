from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib import databrowse
from sunlightapi.api.views import site

admin.autodiscover()

urlpatterns = patterns('',
    (r'^api/$', include('sunlightapi.api.urls')),
    (r'^api/', include(site.urls)),
    (r'^api/admin/(.*)', admin.site.root),
    (r'^api/databrowse/(.*)', databrowse.site.root),
    (r'^api/wordlist/', include('sunlightapi.words.urls')),
)

# currently need views to be imported so that their urls can be inserted
# consider using something similar to admin.autodiscover()
from sunlightapi.legislators import views
from sunlightapi.districts import views
from sunlightapi.lobbyists import views
