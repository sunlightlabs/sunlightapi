from django.contrib.gis.geos import Point
from sunlightapi.api.utils import APIError
from sunlightapi.districts.models import CongressDistrict

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
    districts = CongressDistrict.objects.filter(mpoly__contains=(Point(flng, flat)))

    if len(districts) == 0:
        raise APIError('Point not within a congressional district.')

    return districts
