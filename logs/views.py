from sunlightapi.logs.models import LogEntry
from django.shortcuts import render_to_response


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
