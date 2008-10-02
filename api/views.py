import re
import string
from polipoly import AddressToDistrictService
from Levenshtein import jaro_winkler
from django.core.exceptions import ObjectDoesNotExist
from sunlightapi.api.models import Legislator, ZipDistrict, LegislatorBucket
from sunlightapi.api.utils import apimethod, APIError

RE_TITLES = re.compile('((Congress(wo)?man)|(Sen((ator)|\.)?)|(Rep((resentative)|(\.))?))\s+')

@apimethod('legislators.get')
def legislators_get(params):
    """ Run a query against the Legislators table based on params

        Finds legislator matching constraints passed in params dict
    """
    if params.pop('all_legislators', False) or 'in_office' in params:
        leg = Legislator.all_legislators.get(**params)
    else:
        leg = Legislator.objects.get(**params)
    obj = {'legislator': leg.__dict__}

    return obj

@apimethod('legislators.getList')
def legislators_getlist(params):
    """ Run a query for multiple Legislators based on params

        Finds legislators matching constraints passed in params dict
    """
    if params.pop('all_legislators', False) or 'in_office' in params:
        legislators = Legislator.all_legislators.filter(**params)
    else:
        legislators = Legislator.objects.filter(**params)

    objs = [{'legislator': leg.__dict__} for leg in legislators]
    obj = {'legislators': objs}

    return obj

@apimethod('legislators.allForZip')
def legislators_allforzip(params):
    """ Find all legislators that may represent a given zipcode.

        Typically this means 2 senators and 1 or more representatives.
    """
    zds = ZipDistrict.objects.filter(zip=params['zip'])
    legislators = set()
    states = set()
    for zd in zds:
        legislators.add(Legislator.objects.get(state=zd.state, district=zd.district))
        if zd.state not in states:
            states.add(zd.state)
            legislators.update(Legislator.objects.filter(state=zd.state, title='Sen'))

    objs = [{'legislator': leg.__dict__} for leg in legislators]
    obj = {'legislators': objs}

    return obj

def score_match(str, bucket):
    # the string is flipped to properly prioritize the front of string (Jaro-Winkler)
    if bucket.name_type in (LegislatorBucket.FIRST_LAST, LegislatorBucket.NICK_LAST) and ' ' in str:
        if bucket.name_type == LegislatorBucket.FIRST_LAST:
            bucket.name_type = LegislatorBucket.LAST_FIRST
        else:
            bucket.name_type = LegislatorBucket.LAST_NICK
        str = ' '.join(reversed(str.rsplit(' ',1)))

    leg_name = bucket.get_legislator_name()

    return jaro_winkler(str, leg_name)

@apimethod('legislators.search')
def legislators_search(params):
    """ Attempt to match a Legislator based on their name

        * remove title if one is found (Sen/Rep/Senator/Representative)
        * use (remaining) initials of parameter to get Bucket
        * find via string matching algorithm on all legislators in the Bucket
    """
    name = re.sub('[^a-zA-Z ]', '', params['name'])
    name = string.capwords(name)
    threshold = float(params.get('threshold', 0.8))

    name = RE_TITLES.sub('', name)
    fingerprint = re.sub('[^A-Z]', '', name)

    buckets = LegislatorBucket.objects.filter(bucket=fingerprint)

    # if didn't find them, try extracting the last name
    if not buckets and len(fingerprint) > 1:
        buckets = LegislatorBucket.objects.filter(bucket=fingerprint[-1])
        name = name.rsplit(' ', 1)[-1]

    # get sorted list of scores, and filter those below threshold
    if buckets:
        scores = sorted([(score_match(name, bucket), bucket) for bucket in buckets], reverse=True)
        results = [{'result': {'score': score, 'legislator': bucket.legislator.__dict__}}
            for score,bucket in scores if score > threshold]

        return {'results': results}
    else:
        return {'results': [] }

@apimethod('districts.getDistrictsFromZip')
def districts_from_zip(params):
    """ Return all congressional districts that contain a given zipcode """
    zds = ZipDistrict.objects.filter(zip=params['zip'])
    objs = [{'district': {'state': zd.state, 'number': zd.district}}
            for zd in zds]
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
    lat = params['latitude']
    lng = params['longitude']

    service = AddressToDistrictService('/var/www/django/sunlightapi/congdist/cd99_110')
    lat, lng, districts = service.lat_long_to_district(lat, lng)

    if len(districts) == 0:
        raise APIError('Point not within a congressional district.')

    objs = [{'district': {'state': d[0], 'number': d[1]}} for d in districts]
    obj = {'districts': objs}

    return obj
