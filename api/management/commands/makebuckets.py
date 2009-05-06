from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from sunlightapi.api.models import NameMatchingBucket
from sunlightapi.legislators.models import Legislator, LegislatorBucket
from sunlightapi.lobbyists.models import Lobbyist, LobbyistBucket

def create_buckets(person, bucket_type):

    # first and last initial
    if person.firstname:
        first_initial = person.firstname[0] 
        last_initial = person.lastname[0]
        bucket_type.objects.create(person=person, bucket=first_initial+last_initial,
                                   name_type=NameMatchingBucket.FIRST_LAST)
        bucket_type.objects.create(person=person, bucket=last_initial+first_initial,
                                   name_type=NameMatchingBucket.LAST_FIRST)
        bucket_type.objects.create(person=person, bucket=last_initial,
                                   name_type=NameMatchingBucket.LAST)

    # nickname is optional
    try:
        nick = person.nickname[0]
        bucket_type.objects.create(person=person, bucket=nick+last_initial,
                                   name_type=NameMatchingBucket.NICK_LAST)
        bucket_type.objects.create(person=person, bucket=last_initial+nick,
                                   name_type=NameMatchingBucket.LAST_NICK)
    except (AttributeError, IndexError):
        pass

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--legislators', action='store_true', dest='legislators',
                    default=False, help='refresh legislator buckets'),
        make_option('--lobbyists', action='store_true', dest='lobbyists',
                    default=False, help='refresh lobbyist buckets'),)

    help = "Create the buckets for loose matching of people's names"
    args = ""
    requires_model_validation = False

    def handle(self, *fname, **options):
        legislators = options.get('legislators', False)
        lobbyists = options.get('lobbyists', False)
        # fill all the buckets
        if legislators:
            LegislatorBucket.objects.all().delete()
            for leg in Legislator.all_legislators.all():
                print leg
                create_buckets(leg, LegislatorBucket)

        if lobbyists:
            LobbyistBucket.objects.delete()
            for lobbyist in Lobbyist.objects.all():
                print lobbyist
                create_buckets(lobbyist, LobbyistBucket)
