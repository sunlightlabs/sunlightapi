from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from sunlightapi.api.models import Source

#(?P<format>(\.(xml|json))?)

FORMAT_STR = '(?P<format>(\.(xml|json))?)$'

urlpatterns = patterns('sunlightapi.api.views',
    url(r'^$', direct_to_template,
        {'template': 'index.html',
         'extra_context': { 'sources': Source.objects.all() }} ),

    url(r'^legislators.get%s' % FORMAT_STR, 'legislators_get'),
    url(r'^legislators.getList%s' % FORMAT_STR, 'legislators_getlist'),
    url(r'^legislators.allForZip%s' % FORMAT_STR, 'legislators_allforzip'),
    url(r'^legislators.search%s' % FORMAT_STR, 'legislators_search'),

    url(r'^districts.getDistrictsFromZip%s' % FORMAT_STR, 'districts_from_zip'),
    url(r'^districts.getZipsFromDistrict%s' % FORMAT_STR, 'zips_from_district'),
    url(r'^districts.getDistrictFromLatLong%s' % FORMAT_STR, 'district_from_latlong'),

)
