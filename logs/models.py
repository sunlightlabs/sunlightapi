from django.db import models
from django.newforms import ModelForm

KEY_STATUS = (
    ('U', 'Unactivated'),
    ('A', 'Active'),
    ('S', 'Suspended')
)

class ApiUser(models.Model):

    api_key = models.CharField(max_length=32, primary_key=True)

    email = models.EmailField(unique=True)
    org_name = models.CharField(max_length=100, blank=True)
    org_url = models.URLField(blank=True)
    usage = models.TextField(blank=True)

    signup_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=KEY_STATUS, default='U')

    def active(self):
        return status == 'A'

    def __unicode__(self):
        return '%s (%s)' % (self.email, self.api_key)

    class Admin:
        pass

class ApiUserForm(ModelForm):
    class Meta:
        model = ApiUser
        exclude = ('api_key', 'signup_time', 'status')

class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    method = models.CharField(max_length=50)
    error = models.BooleanField(default=False)
    output = models.CharField(max_length=4)

    caller_key = models.ForeignKey(ApiUser)
    caller_ip = models.IPAddressField()
    caller_host = models.CharField(max_length=100,null=True)
    is_ajax = models.BooleanField()
    query_string = models.CharField(max_length=200,null=True)
