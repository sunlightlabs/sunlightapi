from django.db import models

class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    method = models.CharField(max_length=50)
    error = models.BooleanField(default=False)
    output = models.CharField(max_length=4)

    caller_ip = models.IPAddressField()
    caller_host = models.CharField(max_length=100,null=True)
    is_ajax = models.BooleanField()
    query_string = models.CharField(max_length=200)
