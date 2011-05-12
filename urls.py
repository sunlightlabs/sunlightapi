from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    url(r'^api/$', redirect_to, {'url': 'http://services.sunlightlabs.com/docs/Sunlight_Congress_API/'}),
    url(r'^api/register/$', redirect_to, {'url': 'http://services.sunlightlabs.com/accounts/register/'}),
    (r'^api/', include('locksmith.auth.urls')),
)

# currently need views to be imported so that their urls can be inserted
# consider using something similar to admin.autodiscover()
from sunlightapi.legislators import views
