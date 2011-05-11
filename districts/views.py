import re
from sunlightapi.districts.models import ZipDistrict, CongressDistrict
from sunlightapi.api.utils import apimethod, APIError
from sunlightapi.districts.utils import _district_from_latlong
from sunlightapi import settings

import urllib
try:
    import json
except ImportError:
    import simplejson as json

def _query_boundary_server(**params):
    BOUNDARY_SERVER_URL = 'http://pentagon.sunlightlabs.net/1.0/boundary/?'
    url = BOUNDARY_SERVER_URL + urllib.urlencode(params)
    data = urllib.urlopen(url)
    return json.load(data)

ZIP_RE = re.compile('\d{5}')

@apimethod('districts.getDistrictsFromZip')
def districts_from_zip(params):
    """ Return all congressional districts that contain a given zipcode """

    objs = []

    if ZIP_RE.match(params['zip']):
        result = _query_boundary_server(intersects='zcta-'+params['zip'],
                                        sets='cd')

        # convert objects
        for zobj in result.get('objects', []):
            if '(at Large)' in zobj['name']:
                state = zobj['name'][0:2]
                number = '0'
            else:
                state, number = zobj['name'].split(' Congressional District ')

            objs.append({'district': {'state': state, 'number': number}})

    return {'districts': objs}

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
