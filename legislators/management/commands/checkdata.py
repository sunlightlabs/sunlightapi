from optparse import make_option
import re
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from sunlightapi.legislators.models import Legislator
from votesmart import votesmart, VotesmartApiError
votesmart.apikey = '496ec1875a7885ec65a4ead99579642c'

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
                officials += votesmart.officials.getByOfficeState(6, state)
            except VotesmartApiError:
                officials += []
            officials += votesmart.officials.getByOfficeState(5, state)
        return officials

    def check_legislator_list(self):
        legislators = self.get_legislator_list()
        print len(legislators)
        for leg in legislators:
            try:
                Legislator.objects.get(votesmart_id=leg.candidateId)
            except ObjectDoesNotExist:
                print '%s %s (%s) needs to be added' % (leg.firstName,
                                                        leg.lastName,
                                                        leg.candidateId)

    def update_legislator_list(self):
        for leg in self.get_legislator_list():
            try:
                Legislator.objects.get(votesmart_id=leg.candidateId)
            except ObjectDoesNotExist:
                print 'Adding %s %s (%s)' % (leg.firstName, leg.lastName,
                                             leg.candidateId)
                self.add_legislator(leg)

    def add_legislator(self, official):
        person = {}
        # get basic information
        id = person['votesmart_id'] = official.candidateId
        person['firstname'] = official.firstName
        person['middlename'] = official.middleName
        person['lastname'] = official.lastName
        person['name_suffix'] = official.suffix
        person['nickname'] = official.nickName
        person['title'] = official.title[0:3]
        person['state'] = official.officeStateId
        person['district'] = official.officeDistrictName
        person['party'] = official.officeParties[0]

        # get information from address
        try:
            offices = votesmart.address.getOffice(id)
            for office in offices:
                if office.state == 'DC':
                    person['congress_office'] = office.street
                    person['phone'] = office.phone1
                    person['fax'] = office.fax1
        except VotesmartApiError:
            pass

        # get information from web address
        webaddr_re = re.compile('.+(house|senate)\.gov.+')
        try:
            webaddrs = votesmart.address.getOfficeWebAddress(id)
            for webaddr in webaddrs:
                if webaddr.webAddressType == 'Website' and webaddr_re.match(webaddr.webAddress):
                    person['website'] = webaddr.webAddress
                elif webaddr.webAddressType == 'Webmail' and webaddr_re.match(webaddr.webAddress):
                    person['webform'] = webaddr.webAddress
                elif webaddr.webAddressType == 'Email' and webaddr_re.match(webaddr.webAddress):
                    person['email'] = webaddr.webAddress
        except VotesmartApiError:
            pass

        # get information from bio
        bio = votesmart.candidatebio.getBio(id)
        person['gender'] = bio.gender
        person['fec_id'] = bio.fecId

        pvs_to_bioguide = {4171:'A000364', 23398:'A000365', 79426:'B001265', 45694:'B001263', 104839:'B001264', 93967:'C001079', 69494:'C001075', 103482:'C001076', 1535:'C001077', 95078:'C001078', 102423:'D000608', 45110:'D000609', 108811:'F000456', 110640:'F000455', 68184:'G000556', 60357:'G000557', 18829:'G000558', 21082:'H001049', 9531:'H001044', 101985:'H001045', 74517:'H001046', 106744:'H001047', 104308:'H001048', 18594:'J000290', 21309:'J000291', 28425:'K000368', 57769:'K000369', 12851:'K000370', 101875:'K000371', 4443:'L000567', 110348:'L000568', 20400:'L000569', 102842:'L000570', 15546:'L000571', 68959:'M001171', 106225:'M001172', 69120:'M001173', 9715:'M001177', 44728:'M001174', 23644:'M001176', 436:'M001175', 109342:'N000183', 102008:'O000168', 3833:'P000594', 8749:'P000595', 6586:'P000597', 106220:'P000598', 2919:'R000584', 65306:'R000582', 107800:'R000583', 12023:'S001178', 33428:'S001179', 10813:'S001180', 1663:'S001181', 102408:'T000466', 24046:'T000467', 2629:'T000468', 4403:'T000469', 535:'W000805'}
        
        try:
            person['bioguide_id'] = pvs_to_bioguide[int(id)]

            # leaves out crp_id, bioguide_id, govtrack_id, eventful_id, twitter_id, congresspedia_url
            Legislator.objects.create(**person)
        except KeyError:
            pass
