from django.db import models
from django.forms import ModelForm
from django.forms.util import ValidationError

KEY_STATUS = (
    ('U', 'Unactivated'),
    ('A', 'Active'),
    ('S', 'Suspended')
)


class Method(models.Model):
    """ API Methods - used in sourcing """

    name = models.CharField(max_length=50, primary_key=True)

    def __unicode__(self):
        return self.name


class Source(models.Model):
    """ Sourcing information for API methods """

    name = models.CharField(max_length=50, primary_key=True)
    url = models.URLField()
    last_update = models.DateField()
    source_for = models.ManyToManyField(Method)

    def __unicode__(self):
        return '%s [updated %s]' % (self.name, self.last_update)


    class Meta:
        ordering = ('last_update',)

class ApiUser(models.Model):

    api_key = models.CharField(max_length=32, primary_key=True)

    email = models.EmailField('Email Address', unique=True)
    org_name = models.CharField('Organization Name', max_length=100, blank=True)
    org_url = models.URLField('Organization URL', blank=True)
    usage = models.TextField('Intended Usage', blank=True)

    signup_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=KEY_STATUS, default='U')

    def active(self):
        return status == 'A'

    def __unicode__(self):
        return '%s (%s) [%s]' % (self.email, self.api_key, self.get_status_display())

class ApiUserForm(ModelForm):
    class Meta:
        model = ApiUser
        exclude = ('api_key', 'signup_time', 'status')

    def clean_email(self):
        if ApiUser.objects.filter(email=self.cleaned_data['email']).count():
            raise ValidationError('Email address already registered')
        return self.cleaned_data['email']

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
    
class NameMatchingBucket(models.Model):
    FIRST_LAST = 1
    LAST_FIRST = 2
    LAST = 3
    NICK_LAST = 4
    LAST_NICK = 5
    BUCKET_NAME_TYPE = (
        (FIRST_LAST, 'firstname lastname'),
        (LAST_FIRST, 'lastname firstname'),
        (LAST, 'lastname'),
        (NICK_LAST, 'nickname lastname'),
        (LAST_NICK, 'lastname nickname')
    )
    
    bucket = models.CharField(max_length=5)
    name_type = models.PositiveSmallIntegerField(choices=BUCKET_NAME_TYPE)
    
    def get_legislator_name(self):
        if self.name_type == self.FIRST_LAST:
            return ' '.join([self.person.firstname, self.person.lastname])
        elif self.name_type == self.LAST_FIRST:
            return ' '.join([self.person.lastname, self.person.firstname])
        elif self.name_type == self.LAST:
            return self.person.lastname
        elif self.name_type == self.NICK_LAST:
            return ' '.join([self.person.nickname, self.person.lastname])
        elif self.name_type == self.LAST_NICK:
            return ' '.join([self.person.lastname, self.person.nickname])
        
    def __unicode__(self):
        return '%s is %s of %s' % (self.bucket, self.get_name_type_display(),
                                   self.person)
    
    class Meta:
        abstract = True
