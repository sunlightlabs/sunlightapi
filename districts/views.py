import re
from sunlightapi.districts.models import ZipDistrict, CongressDistrict
from sunlightapi.api.utils import apimethod, APIError
from sunlightapi.districts.utils import _district_from_latlong
from sunlightapi import settings

@apimethod('districts.getDistrictsFromZip')
def districts_from_zip(params):
    """ Return all congressional districts that contain a given zipcode """
    zip_re = re.compile('\d{5}')
    if zip_re.match(params['zip']):
        zds = ZipDistrict.objects.filter(zip=params['zip'])
        objs = [{'district': {'state': zd.state, 'number': zd.district}}
                for zd in zds]
    else:
        objs = []
    obj = {'districts': objs}

    return obj

@apimethod('districts.getZipsFromDistrict')
def zips_from_district(params):
    """ Return all zipcodes within a given congressional district """
    zds = ZipDistrict.objects.filter(state=params['state'],
                                     district=params['district'])

    json_objs = [zd.zip for zd in zds]
    xml_objs = [{'zip':zd.zip} for zd in zds]
    obj = {'json': {'zips': json_objs},
           'xml': {'zips': xml_objs}}

    return obj

@apimethod('districts.getDistrictFromLatLong')
def district_from_latlong(params):
    """ Return the district that a lat/long coordinate pair falls within """
    districts = _district_from_latlong(params)

    objs = [{'district': {'state': d.state_abbrev,
                          'number': int(d.district,10)}} for d in districts]
    obj = {'districts': objs}
    return obj

