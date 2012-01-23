from django.core.management.base import BaseCommand, make_option
from congressapi.models import ZipDistrict

import urllib
try:
    import json
except ImportError:
    import simplejson as json
import time

class Command(BaseCommand):
    help = "update zip-district matching from boundaryservice"

    def handle(self, *args, **options):
        from congressapi.utils import _query_boundary_server
        #clear the list
        #ZipDistrict.objects.all().delete()

        print 'fetching list of ZCTAs...'
        url = 'http://pentagon.sunlightlabs.net/1.0/boundary-set/zcta/'
        data = urllib.urlopen(url).read()
        data = json.loads(data)
        print 'got %s ZCTAs, populating database...' % len(data['boundaries'])

        n = 0

        for boundary in data['boundaries']:

            # pull out zip
            zipcode = boundary[-6:-1]

            if ZipDistrict.objects.filter(zipcode=zipcode).count():
                continue

            # crude progress meter
            n += 1
            if n % 1000 == 0:
                print '%d%% complete..' % (float(n)/len(data['boundaries']))*100

            result = _query_boundary_server(intersects='zcta-'+zipcode,
                                            sets='cd')
            if len(result) == 0:
                print 'Bad ZCTA? %s' % zipcode
            for obj in result:
                ZipDistrict.objects.create(zipcode=zipcode, state=obj['district']['state'],
                                           district=obj['district']['number'])
                time.sleep(0.5)
