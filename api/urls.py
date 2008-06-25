from django.conf.urls.defaults import *

urlpatterns = patterns('sunlightapi.api.views',
    url(r'^legislators.get$', 'legislators_get'),
    url(r'^legislators.getList$', 'legislators_get',
        {'return_list': True}),

    url(r'^districts.getDistrictsFromZip$', 'districts_from_zip'),
    url(r'^districts.getZipsFromDistrict$', 'zips_from_district'),
    url(r'^districts.getDistrictFromLatLong$', 'district_from_latlong'),

)
