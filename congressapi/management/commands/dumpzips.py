import csv
from datetime import datetime
from django.core.management.base import BaseCommand, make_option
from congressapi.models import ZipDistrict

class Command(BaseCommand):
    help = "write zip data to a csv file"

    def handle(self, *fname, **options):
        csvfile = csv.writer(open(fname[0], 'w'))

        for zd in ZipDistrict.objects.all():
            csvfile.writerow((zd.zipcode, zd.state, zd.district))
