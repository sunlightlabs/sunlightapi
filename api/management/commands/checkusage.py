from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from sunlightapi.api.models import KEY_STATUS, ApiUser, LogEntry

class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = "check user statistics"
    args = ""
    requires_model_validation = False

    def handle(self, *fname, **options):
        total = 0
        for code, name in KEY_STATUS:
            count = ApiUser.objects.filter(status=code).count()
            total += count
            print '%d %s users' % (count, name)

        print total, 'total users'

        print LogEntry.objects.all().count(), ' total calls'
