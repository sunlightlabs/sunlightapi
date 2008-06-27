from django.core.exceptions import MultipleObjectsReturned, FieldError, ObjectDoesNotExist
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from sunlightapi.api.models import Source
from sunlightapi.logs.models import LogEntry, ApiUser

""" Utilities for creating API Methods """

class APIError(Exception):
    def __init__(self, message):
        self.message = message


def dict_to_xml(d):
    """ Convert a python dictionary to a simple XML representation

        Dictionary keys create begin/end tags, lists are shown appended together
        and other items are output as they were:

        >>> dict_to_xml({'html':{'ul':[{'li':'uno'}, {'li':'dos'},
                         {'li':'tres'}]}})
        '<html><ul><li>uno</li><li>dos</li><li>tres</li></ul></html>'
    """

    if type(d) == dict:
        return ''.join(['<%s>%s</%s>' % (k,dict_to_xml(v),k)
                        for k,v in d.iteritems()])
    elif type(d) == list:
        return ''.join([dict_to_xml(i) for i in d])
    else:
        return d


def apimethod(method_name):
    """ Decorator to do the repeat work of all api methods.

        Turns request.GET into params and converts return value of func from
        a python object to JSON or XML according to format parameter.
    """
    def decorator(func):
        def newfunc(request, *args, **kwargs):

            format = kwargs.pop('format')

            # preprocess params from request.GET
            params = {}
            metadata = request.GET.get('metadata', None)
            apikey = request.GET.get('apikey', None)
            for key,val in request.GET.iteritems():
                if key not in ('metadata', 'apikey'):
                    params[str(key)] = val[0]

            # do authorization
            try:
                apiuser = ApiUser.objects.get(api_key=apikey, status='A')
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
            except APIError, e:
                error = e.message

            # log this call to the database
            LogEntry.objects.create(method = method_name,
                                    error = bool(error),
                                    output = format,
                                    caller_key = apiuser,
                                    caller_ip = request.META['REMOTE_ADDR'],
                                    caller_host = request.META['REMOTE_HOST'],
                                    is_ajax = request.is_ajax(),
                                    query_string = request.META['QUERY_STRING'])

            # only append metadata if requested & not
            if metadata and not error:
                sources = []
                for s in Source.objects.filter(source_for__name=method_name):
                    sources.append({'source':{'name':s.name, 'url':s.url,
                                    'updated':str(s.last_update)}})
                obj['sources'] = sources

            if not error:
                response = {'response': obj}

                # return obj in correct format (xml or json)'
                if format == '.xml':
                    response = dict_to_xml(response)
                    mimetype = 'application/xml'
                else:
                    response = simplejson.dumps(response)
                    mimetype = 'application/json'

                return HttpResponse(response, mimetype)
            else:
                return HttpResponseBadRequest(error)

        # preserve signature
        newfunc.__name__ = func.__name__
        newfunc.__dict__.update(func.__dict__)
        newfunc.__doc__ = func.__doc__
        newfunc.__module__ = func.__module__

        return newfunc
    return decorator
