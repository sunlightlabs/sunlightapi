from polipoly import AddressToDistrictService
from sunlightapi.districts.models import ZipDistrict
from sunlightapi.api.utils import apimethod, APIError
from sunlightapi import settings

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

    service = AddressToDistrictService(settings.CD_SHAPEFILE)
    try:
        flat, flng = float(lat), float(lng)
    except ValueError:
        raise ApiError('Latitude & Longitude must be floating-point values')
    lat, lng, districts = service.lat_long_to_district(lat, lng)

    if len(districts) == 0:
        raise APIError('Point not within a congressional district.')

    objs = [{'district': {'state': d[0], 'number': d[1]}} for d in districts]
    obj = {'districts': objs}

    return obj
