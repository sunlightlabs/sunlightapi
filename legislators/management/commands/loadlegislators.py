import csv
from datetime import datetime
from django.core.management.base import BaseCommand, make_option
from sunlightapi.legislators.models import Legislator

def dictdiff(a, b):
    keydiff = set(a.keys()).symmetric_difference(set(b.keys()))
    if keydiff:
        print keydiff
    else:
        nodiff = True
        for k,v in a.iteritems():
            if b[k] != v:
                if nodiff:
                    print a['bioguide_id'], a['firstname'], a['lastname']
                nodiff = False
                print '  %s %s --> %s' % (k, v, b[k])

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--save', action='store_true', dest='save',
                    default=False, help='Save changes to database'),)
    help = "update api data from a csv file"

    def handle(self, *fname, **options):
        save = options.get('save', False)
        csvfile = csv.DictReader(open(fname[0]))
        all_legislators = dict([(l.bioguide_id, l) for l in Legislator.all_legislators.all()])

        for line in csvfile:
            line['in_office'] = (line['in_office'] == '1')
            line['birthdate'] = datetime.strptime(line['birthdate'], '%m/%d/%Y').date()
            bioguide = line['bioguide_id']
            leg = all_legislators.get(bioguide)
            if leg:
                ld = dict(leg.__dict__)
                ld.pop('_state')
                dictdiff(ld, line)
                if save:
                    leg.__dict__.update(line)
                    leg.save()
            else:
                print 'new legislator %s %s (%s)' % (line['firstname'], line['lastname'], line['bioguide_id'])
                if save:
                    Legislator.objects.create(**line)
