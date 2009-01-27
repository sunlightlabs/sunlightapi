from django.conf.urls.defaults import *

urlpatterns = patterns('sunlightapi.words.views',
    (r'^(?P<list_name>\w+)/$', 'word_list'),
    (r'^(?P<list_name>\w+)/filter_stopwords/$', 'remove_stopwords'),
)

