from sunlightapi.api.models import Legislator, ZipDistrict
from sunlightapi.api.utils import apimethod, APIError
from polipoly import AddressToDistrictService

@apimethod('legislators.get')
def legislators_get(params, return_list=False):
    """ Run a query against the Legislators table based on params

        Finds legislator(s) matching constraints passed in params dict, unless
        return_list is true restricts results to a single legislator.
    """
    if return_list:
        legislators = Legislator.objects.filter(**params)
        objs = []
        for leg in legislators:
            obj = {'legislator': leg.__dict__}
            objs.append(obj)
        obj = {'legislators': objs}
    else:
        leg = Legislator.objects.get(**params)
        obj = {'legislator': leg.__dict__}

    return obj

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

    objs = [zd.zip for zd in zds]
    obj = {'zips': objs}

    return obj

@apimethod('districts.getDistrictFromLatLong')
def district_from_latlong(params):
    """ Return the district that a lat/long coordinate pair falls within """
    lat = params['latitude']
    lng = params['longitude']

    service = AddressToDistrictService('congdist/cd99_110')
    lat, lng, districts = service.lat_long_to_district(lat, lng)

    if len(districts) == 0:
        raise APIError('Point not within a congressional district.')

    objs = [{'district': {'state': d[0], 'number': d[1]}} for d in districts]
    obj = {'districts': objs}

    return obj
