from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
from locksmith.auth.models import ApiKey

class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    method = models.CharField(max_length=50)
    error = models.BooleanField(default=False)
    output = models.CharField(max_length=4)

    caller_key = models.ForeignKey(ApiKey)
    caller_ip = models.IPAddressField()
    query_string = models.CharField(max_length=200,null=True)

    class Meta:
        db_table = "api_logentry"


# choices for party
PARTIES = (
    ('D', 'Democrat'),
    ('I', 'Independent'),
    ('R', 'Republican'))

# short and long form of titles
TITLES = (
    ('Rep', 'Representative'),
    ('Sen', 'Senator'),
    ('Del', 'Delegate'),
    ('Com', 'Resident Commissioner'))

# short and long form of genders
GENDERS = (
    ('F', 'Female'),
    ('M', 'Male'))

class ActiveLegislatorManager(models.Manager):
    def get_query_set(self):
        return super(ActiveLegislatorManager, self).get_query_set().filter(in_office=True)

class AllLegislatorManager(models.Manager):
    def get_query_set(self):
        return super(AllLegislatorManager, self).get_query_set()

class Legislator(models.Model):
    """ Model containing basic information for legislators """

    all_legislators = AllLegislatorManager()
    objects = ActiveLegislatorManager()

    # name
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30)
    name_suffix = models.CharField(max_length=5, blank=True)
    nickname = models.CharField(max_length=30, blank=True)

    # job
    title = models.CharField(max_length=3, choices=TITLES)
    state = models.CharField(max_length=2)
    district = models.CharField(max_length=12)
    party = models.CharField(max_length=1, choices=PARTIES)
    in_office = models.BooleanField(default=True)

    # contact info
    congress_office = models.CharField(max_length=50, blank=True)
    phone = PhoneNumberField(blank=True)
    fax = PhoneNumberField(blank=True)
    website = models.URLField(blank=True)
    webform = models.URLField(blank=True)

    # other info
    gender = models.CharField(max_length=1, choices=GENDERS)
    birthdate = models.DateField()
    senate_class = models.CharField(max_length=3)

    # other site ids
    votesmart_id = models.CharField(max_length=20, blank=True)
    fec_id = models.CharField(max_length=20)
    crp_id = models.CharField(max_length=20)
    bioguide_id = models.CharField(max_length=20, primary_key=True)
    govtrack_id = models.CharField(max_length=20)
    twitter_id = models.CharField(max_length=20, blank=True)
    facebook_id = models.CharField(max_length=50, blank=True)
    congresspedia_url = models.URLField()
    youtube_url = models.URLField(blank=True)
    official_rss = models.URLField(blank=True)

    def __unicode__(self):
        return '%s %s (%s-%s)' % (self.get_title_display(), self.lastname,
                                  self.party, self.state)

    class Meta:
        ordering = ('lastname', 'firstname')
        db_table = "legislators_legislator"

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

class LegislatorBucket(NameMatchingBucket):
    person = models.ForeignKey(Legislator)

    class Meta:
        db_table = "legislators_legislatorbucket"

CHAMBERS = (('House', 'House'),('Senate','Senate'))

class Committee(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    chamber = models.CharField(max_length=6, choices=CHAMBERS)
    parent = models.ForeignKey('self', related_name='subcommittees', null=True)
    name = models.CharField(max_length=300)
    members = models.ManyToManyField(Legislator, related_name='committees')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "legislators_committee"
