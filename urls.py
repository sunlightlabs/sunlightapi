from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^api/', include('sunlightapi.api.urls')),
    (r'^api/', include('locksmith.auth.urls')),
)

# currently need views to be imported so that their urls can be inserted
# consider using something similar to admin.autodiscover()
from sunlightapi.legislators import views
from sunlightapi.districts import views
