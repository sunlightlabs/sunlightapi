from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from sunlightapi.api.models import Legislator, LegislatorBucket

BUCKET_NAME_TYPE = (
    (1, 'firstname lastname'),
    (2, 'lastname firstname'),
    (3, 'lastname'),
    (4, 'nickname lastname'),
    (5, 'lastname nickname')
)

class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = 'Create the buckets for loose matching of legislators'
    args = ''
    requires_model_validation = False

    def handle(self, *fname, **options):
        # fill all the buckets
        for leg in Legislator.objects.all():
            print leg
            LegislatorBucket.objects.create(legislator=leg, bucket=leg.firstname[0] + leg.lastname[0], name_type=1)
            LegislatorBucket.objects.create(legislator=leg, bucket=leg.lastname[0] + leg.firstname[0], name_type=2)
            LegislatorBucket.objects.create(legislator=leg, bucket=leg.lastname[0], name_type=3)
            if leg.nickname:
                LegislatorBucket.objects.create(legislator=leg, bucket=leg.nickname[0] + leg.lastname[0], name_type=4)
                LegislatorBucket.objects.create(legislator=leg, bucket=leg.lastname[0] + leg.nickname[0], name_type=5)
