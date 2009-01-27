from django.conf.urls.defaults import *

urlpatterns = patterns('words.views',
    (r'^wordlist/(?P<list_name>\w+)/$', 'word_list'),
    (r'^remove_stopwords/(?P<list_name>\w+)/$', 'remove_stopwords'),
)

