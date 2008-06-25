from django.views.generic.list_detail import object_list
from django.conf.urls.defaults import *
from sunlightapi.logging.models import LogEntry

urlpatterns = patterns('',
    url(r'^raw/(?P<page>\d+)/$', object_list,
        {'queryset': LogEntry.objects.all(),
         'paginate_by': 100,
         'template_name': 'log_raw.html',
         }),
    url(r'^summary/$', 'logging.views.summary'),
)
