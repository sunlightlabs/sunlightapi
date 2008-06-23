#!/usr/bin/env python
import cjson
#from votesmart import VoteSmart
from api.models import Legislator
from django.core.exceptions import ObjectDoesNotExist

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA',
          'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD','MA', 'MI',
          'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
          'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
          'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'PR' ]
#pvs = VoteSmart('496ec1875a7885ec65a4ead99579642c')

def check_missing_data():
    required_fields = ('firstname', 'lastname', 'title', 'state', 'party',
                       'congress_office', 'phone', 'fax', 'website', 'gender',
                       'votesmart_id', 'fec_id', 'bioguide_id', 'govtrack_id',
                       'congresspedia_url')
    for leg in Legislator.objects.all():
        for field in required_fields:
            if not leg.__dict__[field]:
                print '%s is missing %s' % (leg, field)

def get_legislator_list():
    # get all state officials
    try:
        sen = pvs.Officials.getByOfficeState(6, state)['candidateList']['candidate']
    except KeyError:
        sen = []
    rep = pvs.Officials.getByOfficeState(5, state)['candidateList']['candidate']
    if type(rep) == dict:
        rep = [rep]
    return sen + rep

def check_legislator_list():
    for leg in get_legislator_list():
        try:
            Legislator.objects.get(pvs_id=leg['candidateId'])
        except ObjectDoesNotExist:
            print '%s %s (%s) needs to be added' % (leg['firstName'],
                                                    leg['lastName'],
                                                    leg['candidateId'])

def add_legislator(id):
    person = {}
    # get basic information
    person['votesmart_id'] = official['candidateId']
    person['firstname'] = official['firstName']
    person['lastname'] = official['lastName']
    person['middlename'] = official['middleName']
    person['nickname'] = official['nickName']
    person['name_suffix'] = official['suffix']
    person['party'] = official['officeParties'][0]
    person['state'] = official['officeStateId']
    person['title'] = official['title'][0:3]

    # get information from address
    try:
        offices = pvs.Address.getOffice(id)['address']['office']
        if type(offices) != list:
            offices = [offices]
        for office in offices:
            if office['address']['state'] == 'DC':
                person['congress_office'] = office['address']['street']
                person['phone'] = office['phone']['phone1']
                person['fax'] = office['phone']['fax1']
    except KeyError:
        pass

    # get information from web address
    webaddr_re = re.compile('.+(house|senate)\.gov.+')
    try:
        webaddrs = pvs.Address.getOfficeWebAddress(id)['webaddress']['address']
        if type(webaddrs) != list:
            webaddrs = [webaddrs]
        for webaddr in webaddrs:
            if webaddr['webAddressType'] == 'Website' and webaddr_re.match(person['website']):
                person['website'] = webaddr['webAddress']
            elif webaddr['webAddressType'] == 'Webmail' and webaddr_re.match(person['website']):
                person['webform'] = webaddr['webAddress']
            elif webaddr['webAddressType'] == 'Email' and webaddr_re.match(person['website']):
                person['email'] = webaddr['webAddress']
    except KeyError:
        pass

    # get information from bio
    bio = pvs.CandidateBio.getBio(id)['bio']
    person['fec_id'] = bio['candidate']['fecId']
    person['gender'] = bio['candidate']['gender']
    person['district'] = bio['office']['district']
