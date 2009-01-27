from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^wordlist/(?P<list_name>\w+)/$', 'words.views.word_list'),
)

