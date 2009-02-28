import md5
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
import datetime
from sunlightapi.api.models import LogEntry, ApiUser, ApiUserForm

def register(request):
    if request.method == 'POST':
        form = ApiUserForm(request.POST)
        if form.is_valid():
            newuser = form.save(commit=False)
            newuser.api_key = md5.new(newuser.email + 'sunlightapi').hexdigest()
            newuser.last_email_sent = datetime.datetime.now()
            newuser.save()
            message = '''Thank you for registering for a Sunlight Labs API Key.

Please visit the following URL to verify your email address and activate your key
http://services.sunlightlabs.com/api/confirmkey/%s/

Your details are included below for your records:
    Email: %s
    API Key: %s
    Organization Name: %s
    Organization URL: %s
    Usage: %s
    Signup Time: %s''' % (newuser.api_key, newuser.email, newuser.api_key,
                          newuser.org_name, newuser.org_url, newuser.usage,
                          newuser.signup_time)
            send_mail('Sunlight API Registration', message,
                      'api@sunlightlabs.com', [newuser.email])
            return render_to_response('registered.html', {'user': newuser})
    else:
        form = ApiUserForm()
    return render_to_response('register.html', {'form': form})

def confirm_registration(request, apikey):
    error = None
    try:
        user = ApiUser.objects.get(pk=apikey)
        if user.status != 'U':
            error = 'Key Already Activated'
        else:
            user.status = 'A'
            user.save()
    except ObjectDoesNotExist:
        error = 'Invalid Key'
        user = None
    return render_to_response('confirmed.html',
                              {'error': error, 'user': user})

def summary(request):
    from django.db import connection
    cursor = connection.cursor()
    stats = {}
    cursor.execute("SELECT method,COUNT(*) FROM logs_logentry GROUP BY method")
    stats['methods'] = cursor.fetchall()
    #cursor.execute("SELECT error,COUNT(*) FROM logs_logentry GROUP BY error")
    #stats['errors'] = cursor.fetchall()
    cursor.execute("SELECT output,COUNT(*) FROM logs_logentry GROUP BY output")
    stats['outputs'] = cursor.fetchall()
    #cursor.execute("SELECT is_ajax,COUNT(*) FROM logs_logentry GROUP BY is_ajax")
    #stats['ajax'] = cursor.fetchall()
    cursor.execute("SELECT COUNT(*),STRFTIME('%%m-%%Y',timestamp) FROM logs_logentry GROUP BY strftime('%%m-%%Y',timestamp)")
    stats['months'] = cursor.fetchall()
    return render_to_response('log_summary.html', stats)
