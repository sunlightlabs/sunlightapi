from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from sunlightapi.api.models import Source

#(?P<format>(\.(xml|json))?)

urlpatterns = patterns('sunlightapi.api.views',
    url(r'^$', direct_to_template,
        {'template': 'index.html',
         'extra_context': { 'sources': Source.objects.all() }} ),

    url(r'^legislators.get(?P<format>(\.(xml|json))?)$', 'legislators_get'),
    url(r'^legislators.getList(?P<format>(\.(xml|json))?)$', 'legislators_getlist'),

    url(r'^districts.getDistrictsFromZip(?P<format>(\.(xml|json))?)$', 'districts_from_zip'),
    url(r'^districts.getZipsFromDistrict(?P<format>(\.(xml|json))?)$', 'zips_from_district'),
    url(r'^districts.getDistrictFromLatLong(?P<format>(\.(xml|json))?)$', 'district_from_latlong'),

)
