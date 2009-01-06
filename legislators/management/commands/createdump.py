from optparse import make_option
import gzip
from types import UnicodeType
from csv import DictWriter
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from sunlightapi.api.models import Legislator

class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = 'Create a tarball containing all of the Legislator data in the API'
    args = 'filename'
    requires_model_validation = False

    def handle(self, *fname, **options):
        if len(fname) != 1:
            raise CommandError('Must provide a filename for the dump')
        self.csv_dump(fname[0])

    def csv_dump(self, filename):
        keys = ['title', 'firstname', 'middlename', 'lastname', 'name_suffix',
                'nickname', 'party', 'state', 'district', 'in_office',
                'gender', 'phone', 'fax', 'website', 'webform', 'email',
                'congress_office', 'bioguide_id', 'votesmart_id', 'fec_id',
                'govtrack_id', 'crp_id', 'eventful_id', 'sunlight_old_id',
                'twitter_id', 'congresspedia_url']
        writer = DictWriter(gzip.open(filename, 'w'), keys)
        headernames = dict(zip(keys, keys))
        writer.writerow(headernames)

        for leg in Legislator.all_legislators.all():
            utf8dict = {}
            for k,v in leg.__dict__.iteritems():
                if isinstance(v, UnicodeType):
                    v = v.encode('utf-8')
                utf8dict[k] = v
            writer.writerow(utf8dict)
