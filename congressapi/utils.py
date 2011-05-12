""" Utilities for creating API Methods """

import urllib
try:
    import json
except ImportError:
    import simplejson as json

from django.core.exceptions import MultipleObjectsReturned, FieldError, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.core.urlresolvers import get_resolver
from django.conf.urls.defaults import url
from django.conf import settings
from jellyfish import jaro_winkler
from congressapi.models import NameMatchingBucket, LogEntry
from locksmith.auth.models import ApiKey

_api_urls = get_resolver(None).url_patterns

FORMAT_STR = '(?P<format>(\.(xml|json))?)$'

class APIError(Exception):
    def __init__(self, message):
        self.message = message


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


def dict_to_xml(d):
    """ Recursively convert a python dictionary to a simple XML representation

        Dictionary keys create begin/end tags, lists are shown appended together
        with spaces and other items are output as they were:

        >>> dict_to_xml({'html':{'ul':[{'li':'uno'}, {'li':'dos'},
                         {'li':'tres'}]}})
        '<html><ul><li>uno</li><li>dos</li><li>tres</li></ul></html>'
    """

    if isinstance(d, dict):
        return ''.join(['<%s>%s</%s>' % (k,dict_to_xml(v),k)
                        for k,v in d.iteritems()])
    elif isinstance(d, list):
        return ' '.join([dict_to_xml(i) for i in d])
    elif d is None:
        return ''
    else:
        return d


def score_match(str, bucket):
    # the string is flipped to properly prioritize the front of string (due to requirements of Jaro-Winkler)
    if bucket.name_type in (NameMatchingBucket.FIRST_LAST, NameMatchingBucket.NICK_LAST) and ' ' in str:
        if bucket.name_type == NameMatchingBucket.FIRST_LAST:
            bucket.name_type = NameMatchingBucket.LAST_FIRST
        else:
            bucket.name_type = NameMatchingBucket.LAST_NICK
        str = ' '.join(reversed(str.rsplit(' ',1)))

    name = bucket.get_person_name()

    return jaro_winkler(str, name)

def make_serializable(obj):
    from datetime import date
    if isinstance(obj, date):
        return str(obj)
    else:
        raise TypeError

def apimethod(method_name):
    """ Decorator to do the repeat work of all api methods.

        Turns request.GET into params and converts return value of func from
        a python object to JSON or XML according to format parameter.
    """

    def decorator(func):
        def newfunc(request, *args, **kwargs):

            format = kwargs.pop('format')
            if format:
                format = format[1:]
            else:
                format = 'json'

            # preprocess params from request.GET
            params = {}
            apikey = request.GET.get('apikey', None)
            jsonp = request.GET.get('jsonp', None)
            for key,val in request.GET.lists():
                if key not in ('metadata', 'apikey', 'jsonp'):
                    # unlistify single items
                    if len(val) == 1:
                        params[str(key)] = val[0]
                    else:
                        params[str(key)+'__in'] = val

            # do authorization
            try:
                apiuser = ApiKey.objects.get(key=apikey, status='A')
            except ObjectDoesNotExist:
                return HttpResponseForbidden('Invalid API Key')

            # call the actual api function
            error = None
            try:
                obj = func(params, *args, **kwargs)
            except KeyError, e:
                error = 'Missing Parameter: %s' % e
            except FieldError, e:
                error = 'Invalid Parameter'
            except MultipleObjectsReturned, e:
                error = 'Multiple Legislators Returned'
            except ObjectDoesNotExist, e:
                error = 'No Such Object Exists'
            except APIError, e:
                error = e.message

            # log this call to the database
            LogEntry.objects.create(method = method_name,
                                    error = bool(error),
                                    output = format,
                                    caller_key = apiuser,
                                    caller_ip = request.META['REMOTE_ADDR'],
                                    query_string = request.META['QUERY_STRING'])

            if not error:
                # replace obj with obj['xml'] or obj['json'] if they exist
                obj = obj.get(format, obj)

                response = {'response': obj}

                # return obj in correct format (xml or json)'
                if format == 'xml':
                    response = dict_to_xml(response).replace('&', '&amp;')
                    mimetype = 'application/xml'
                else:
                    response = json.dumps(response, default=make_serializable)
                    if jsonp:
                        response = '%s(%s)' % (jsonp, response)
                        mimetype = 'text/javascript'
                    else:
                        mimetype = 'application/json'

                return HttpResponse(response, mimetype)
            elif error and jsonp:
                response = '%s({"error": "%s"})' % (jsonp, error)
                return HttpResponse(response, 'text/javascript')
            else:
                return HttpResponseBadRequest(error)

        # preserve signature
        newfunc.__name__ = func.__name__
        newfunc.__dict__.update(func.__dict__)
        newfunc.__doc__ = func.__doc__
        newfunc.__module__ = func.__module__

        # append url to patterns
        _api_urls.append(url(r'^%s%s%s' % (settings.API_URL_BASE, method_name,
                                           FORMAT_STR), newfunc))

        return newfunc

    return decorator
