from django.db import models
from locksmith.auth.models import ApiKey

class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    method = models.CharField(max_length=50)
    error = models.BooleanField(default=False)
    output = models.CharField(max_length=4)

    caller_key = models.ForeignKey(ApiKey)
    caller_ip = models.IPAddressField()
    query_string = models.CharField(max_length=200,null=True)
