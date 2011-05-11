import re
from sunlightapi.api.utils import apimethod, APIError
from sunlightapi.districts.utils import (_query_boundary_server,
                                         _districts_from_zip,
                                         _district_from_latlong)

ZIP_RE = re.compile('\d{5}')

@apimethod('districts.getDistrictsFromZip')
def districts_from_zip(params):
    """ Return all congressional districts that contain a given zipcode """

    objs = []

    if ZIP_RE.match(params['zip']):
        _districts_from_zip(params['zip'])

    return {'districts': objs}


@apimethod('districts.getZipsFromDistrict')
def zips_from_district(params):
    """ Return all zipcodes within a given congressional district """
    raise APIError("districts.getZipsFromDistrict is no longer supported")


@apimethod('districts.getDistrictFromLatLong')
def district_from_latlong(params):
    """ Return the district that a lat/long coordinate pair falls within """
    objs = _district_from_latlong(params)
    return {'districts': objs}
