import re
import string
from polipoly import AddressToDistrictService
from django.core.exceptions import ObjectDoesNotExist
from sunlightapi.legislators.models import Legislator, LegislatorBucket, Committee
from sunlightapi.districts.models import ZipDistrict
from sunlightapi.api.utils import apimethod, APIError, score_match

RE_TITLES = re.compile(r'((Congress(wo)?man)|(Sen((ator)|\.)?)|(Rep((resentative)|(\.))?))\s+')
RE_SUFFIX = re.compile(r'\b(Jr|Junior|Ii|Iii|Iv)\b')

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
    name = RE_SUFFIX.sub('', name)
    fingerprint = re.sub('[^A-Z]', '', name)

    buckets = LegislatorBucket.objects.filter(bucket=fingerprint).select_related()

    # if didn't find them, try extracting the last name
    if not buckets and len(fingerprint) > 1:
        buckets = LegislatorBucket.objects.filter(bucket=fingerprint[-1])
        name = name.rsplit(' ', 1)[-1]

    # get sorted list of scores, and filter those below threshold
    if buckets:
        scores = sorted([(score_match(name, bucket), bucket) for bucket in buckets], reverse=True)
        results = [{'result': {'score': score, 'legislator': bucket.person.__dict__}}
            for score,bucket in scores if score > threshold]

        return {'results': results}
    else:
        return {'results': []}


@apimethod('committees.get')
def committees_get(params):
    """ Get details for a committee, including subcommittees and legislators. """
    com_id = params['id']
    committee = Committee.objects.get(pk=com_id)
    result = {'committee': committee.__dict__,
              'subcommittees': [{'committee': c.__dict__} for c in committee.subcommittees.all()],
              'members': [{'legislator': m.__dict__} for m in committee.members.all()]}
    return result

@apimethod('committees.getList')
def committees_getlist(params):
    """ Get a list of legislators for a chamber or committee.

        If chamber is specified then all top level committees are returned.
        If committee is specified then all subcommittees are returned.
    """

    chamber = params.get('chamber')
    committee = params.get('committee')
    
    if chamber and committee:
        raise APIError('must specify chamber OR committee parameter')
    elif chamber:
        committees = Committee.objects.filter(chamber=chamber, parent=None)
    elif committee:
        committees = Committee.objects.filter(parent=committee)
    else:
        raise APIError('must specify chamber or committee parameter')

    return {'committees': [{'committee': c.__dict__} for c in committees]}

@apimethod('committees.allForLegislator')
def committees_allforlegislator(params):
    """ Get a listing of all committees that a legislator belongs to """
    bioguide_id = params['bioguide_id']
    legislator = Legislator.objects.get(pk=bioguide_id)
    committees = legislator.committees.all()
    return {'committees': [{'committee': c.__dict__} for c in committees]}
