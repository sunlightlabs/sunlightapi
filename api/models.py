from django.db import models
from django.forms import ModelForm
from django.forms.util import ValidationError
from locksmith.auth.models import Key

class ApiUser(Key):
    org_name = models.CharField('Organization Name', max_length=100, blank=True)
    org_url = models.URLField('Organization URL', blank=True)
    usage = models.TextField('Intended Usage', blank=True)

class ApiUserForm(ModelForm):
    class Meta:
        model = ApiUser
        exclude = ('key', 'issued_on', 'status')

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
    
    def get_person_name(self):
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
