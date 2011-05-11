from sunlightapi.api.utils import APIError

import urllib
try:
    import json
except ImportError:
    import simplejson as json

def _query_boundary_server(**params):
    BOUNDARY_SERVER_URL = 'http://pentagon.sunlightlabs.net/1.0/boundary/?'
    url = BOUNDARY_SERVER_URL + urllib.urlencode(params)
    data = urllib.urlopen(url)
    result = json.load(data)

    objs = []
    for zobj in result.get('objects', []):
        if '(at Large)' in zobj['name']:
            state = zobj['name'][0:2]
            number = '0'
        else:
            state, number = zobj['name'].split(' Congressional District ')

        objs.append({'district': {'state': state, 'number': number}})
    return objs

def _districts_from_zip(zip):
    return _query_boundary_server(intersects='zcta-'+zip, sets='cd')

def _district_from_latlong(params):
    lat = params['latitude']
    lng = params['longitude']

    try:
        flat, flng = float(lat), float(lng)
    except ValueError:
        raise APIError('Latitude & Longitude must be floating-point values')
    # force longitude to western hemisphere
    if flng > 0:
        flng = -flng

    districts = _query_boundary_server(contains='%s,%s' % (flat, flng),
                                       sets='cd')

    if len(districts) == 0:
        raise APIError('Point not within a congressional district.')

    return districts
