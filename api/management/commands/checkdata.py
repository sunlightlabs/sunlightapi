from optparse import make_option
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from sunlightapi.api.models import Legislator
from votesmart import VoteSmart

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--missing-data', action='store_true', dest='missing',
                    default=False,
                    help='Check for missing data on existing legislators'),
        make_option('--legislators', action='store_true', dest='legislators',
                    default=False, help='Check for new legislators'),
        make_option('--update', action='store_true', dest='update',
                    default=False, help='Add new legislators'),
    )
    help = 'Check and update API data'
    args = ''
    requires_model_validation = False

    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA',
              'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
              'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
              'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
              'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'PR' ]
    pvs = VoteSmart('496ec1875a7885ec65a4ead99579642c')

    def handle(self, *args, **options):
        missing = options.get('missing', False)
        legislators = options.get('legislators', False)
        update = options.get('update', False)

        if legislators:
            self.check_legislator_list()
        if update:
            self.update_legislator_list()
        if missing:
            self.check_missing_data()

        if not (legislators or update or missing):
            print 'Please specify at least one option.'

    def check_missing_data(self):
        required_fields = ('firstname', 'lastname', 'title', 'state', 'party',
                           'congress_office', 'phone', 'fax', 'website', 'gender',
                           'votesmart_id', 'fec_id', 'bioguide_id', 'govtrack_id',
                           'congresspedia_url')
        for leg in Legislator.objects.all():
            for field in required_fields:
                if not leg.__dict__[field]:
                    print '%s is missing %s' % (leg, field)

    def get_legislator_list(self):
        # get all state officials
        officials = []
        for state in self.states:
            print state
            try:
                sen = self.pvs.Officials.getByOfficeState(6, state)['candidateList']['candidate']
            except KeyError:
                sen = []
            rep = self.pvs.Officials.getByOfficeState(5, state)['candidateList']['candidate']
            if type(rep) == dict:
                rep = [rep]
            officials.append(sen).append(rep)
        return officials

    def check_legislator_list(self):
        for leg in self.get_legislator_list():
            try:
                Legislator.objects.get(pvs_id=leg['candidateId'])
            except ObjectDoesNotExist:
                print '%s %s (%s) needs to be added' % (leg['firstName'],
                                                        leg['lastName'],
                                                        leg['candidateId'])

    def update_legislator_list(self):
        for leg in get_legislator_list():
            try:
                Legislator.objects.get(pvs_id=leg['candidateId'])
            except ObjectDoesNotExist:
                print 'Adding %s %s (%s)' % (leg['firstName'], leg['lastName'],
                                             leg['candidateId'])
                add_legislator(leg)

    def add_legislator(self, official):
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

        Legislator.objects.create(person)
