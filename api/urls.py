from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^legislators.get$', 'api.views.legislators_get'),
    url(r'^legislators.getList$', 'api.views.legislators_get',
        {'return_list': True}),

    url(r'^districts.getDistrictsFromZip$', 'api.views.districts_from_zip'),
    url(r'^districts.getZipsFromDistrict$', 'api.views.zips_from_district'),
    url(r'^districts.getDistrictFromLatLong$',
        'api.views.district_from_latlong'),

)
