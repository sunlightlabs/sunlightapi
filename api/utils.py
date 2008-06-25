from django.core.exceptions import MultipleObjectsReturned, FieldError
from django.utils import simplejson
from django.http import HttpResponse
from sunlightapi.api.models import Source
from sunlightapi.logging.models import LogEntry

""" Utilities for creating API Methods """

class APIError(Exception):
    def __init__(self, code, message):
        self.message = message
        self.code = code


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
        a python object to JSON or XML according to output parameter.
    """
    def decorator(func):
        def newfunc(request, *args, **kwargs):
            # preprocess params from request.GET
            params = {}
            output = request.GET.get('output', 'json')
            metadata = request.GET.get('metadata', None)
            for key,val in request.GET.iteritems():
                if key not in ('output', 'metadata'):
                    params[str(key)] = val[0]

            # call the actual api function
            try:
                obj = func(params, *args, **kwargs)
            except KeyError, e:
                obj = {'error': {'code': 101,
                                 'message':'Missing Parameter: %s' % e}}
            except FieldError, e:
                obj = {'error': {'code': 102,
                                 'message':'Invalid Parameter'}}
            except MultipleObjectsReturned, e:
                obj = {'error': {'code': 103,
                                 'message':'Multiple Objects Returned'}}
            except APIError, e:
                obj = {'error': {'code': e.code, 'message':e.message}}

            # only append metadata if requested & return value not an error
            if metadata and not obj.has_key('error'):
                sources = []
                for s in Source.objects.filter(source_for__name=method_name):
                    sources.append({'source':{'name':s.name, 'url':s.url,
                                    'updated':str(s.last_update)}})
                obj['sources'] = sources

            response = {'response': obj}

            # log this call to the database
            LogEntry.objects.create(method = method_name,
                                    error = obj.has_key('error'),
                                    output = output,
                                    caller_ip = request.META['REMOTE_ADDR'],
                                    caller_host = request.META['REMOTE_HOST'],
                                    is_ajax = request.is_ajax(),
                                    query_string = request.META['QUERY_STRING'])

            # return obj in correct format (xml or json)'
            if output == 'xml':
                response = dict_to_xml(response)
                mimetype = 'application/xml'
            else:
                response = simplejson.dumps(response)
                mimetype = 'application/json'
            return HttpResponse(response, mimetype)

        # preserve signature
        newfunc.__name__ = func.__name__
        newfunc.__dict__.update(func.__dict__)
        newfunc.__doc__ = func.__doc__
        newfunc.__module__ = func.__module__

        return newfunc
    return decorator
