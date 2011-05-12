from django.core.management.base import BaseCommand, make_option
from congressapi.models import Legislator, Committee
import urllib
import lxml.html

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--save', action='store_true', dest='save',
                    default=False, help='Save changes to database'),)
    help = "update committee data from govtrack's XML"

    def handle(self, *fname, **options):
        save = options.get('save', False)
        GOVTRACK_URL = 'http://govtrack.us/data/us/112/committees.xml'

        data = urllib.urlopen(GOVTRACK_URL).read()
        doc = lxml.html.fromstring(data)

        legislators = dict((l.govtrack_id, l)
                           for l in Legislator.objects.all())

        Committee.objects.all().delete()

        for com in doc.xpath('//committee'):
            com_id = com.get('code')
            com_chamber = com.get('type').capitalize()
            com_obj = Committee.objects.create(id=com_id,
                                               chamber=com_chamber,
                                               parent=None,
                                               name=com.get('displayname').strip())
            for m in com.xpath('member/@id'):
                com_obj.members.add(legislators[m])

            for sc in com.xpath('subcommittee'):
                sc_obj = Committee.objects.create(id='%s_%s' % (com_id, sc.get('code')),
                                                  chamber=com_chamber,
                                                  parent=com_obj,
                                                  name=sc.get('displayname').strip())
                for m in sc.xpath('member/@id'):
                    sc_obj.members.add(legislators[m])
