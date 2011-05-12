from django.core.management.base import BaseCommand

from congressapi.models import Legislator, LegislatorBucket, NameMatchingBucket

def create_buckets(person, bucket_type):

    # first and last initial
    if person.firstname:
        first_initial = person.firstname[0]
        last_initials = ''.join(n[0] for n in person.lastname.split())
        bucket_type.objects.create(person=person, bucket=first_initial+last_initials,
                                   name_type=NameMatchingBucket.FIRST_LAST)
        bucket_type.objects.create(person=person, bucket=last_initials+first_initial,
                                   name_type=NameMatchingBucket.LAST_FIRST)
        bucket_type.objects.create(person=person, bucket=last_initials,
                                   name_type=NameMatchingBucket.LAST)

    # nickname is optional
    try:
        nick = person.nickname[0]
        bucket_type.objects.create(person=person, bucket=nick+last_initials,
                                   name_type=NameMatchingBucket.NICK_LAST)
        bucket_type.objects.create(person=person, bucket=last_initials+nick,
                                   name_type=NameMatchingBucket.LAST_NICK)
    except (AttributeError, IndexError):
        pass


class Command(BaseCommand):
    help = "Create the buckets for loose matching of people's names"
    args = ""
    requires_model_validation = False

    def handle(self, *fname, **options):
        LegislatorBucket.objects.all().delete()
        for leg in Legislator.all_legislators.all():
            print leg
            create_buckets(leg, LegislatorBucket)
