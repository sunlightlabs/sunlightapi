from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from sunlightapi.api.models import KEY_STATUS, ApiUser, LogEntry
import datetime

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--email', action='store_true', dest='email',
                    default=False, help='Email Unactivated Users'),)
    help = "check user statistics"
    args = ""
    requires_model_validation = False

    def handle(self, *fname, **options):
        email = options.get('email', False)

        total = 0
        for code, name in KEY_STATUS:
            count = ApiUser.objects.filter(status=code).count()
            total += count
            print '%d %s users' % (count, name)

        print total, 'total users'

        print LogEntry.objects.all().count(), ' total calls'

        if email:
            for u in ApiUser.objects.filter(status='U'):
                last_email = u.last_email_sent - datetime.datetime.now()
                if last_email < datetime.timedelta(days=-30):
                    body = '''Hi,
        We noticed that you signed up for a Sunlight Labs API Key on %s-%s-%s and haven't activated it.

        Just to remind you, you can activate your key by visiting http://services.sunlightlabs.com/api/confirmkey/%s/
        If you do not activate your key within 30 days it will be deleted.''' % (u.signup_time.month, u.signup_time.day, u.signup_time.year, u.api_key)

                    send_mail('Sunlight Labs API Registration', body, 'api@sunlightlabs.com', [u.email])
                    print 'email sent to', u.email
                    u.last_email_sent = datetime.datetime.now()
                    u.save()
                else:
                    print 'no email sent to %s, last email sent %s' % (u.email, u.last_email_sent)
