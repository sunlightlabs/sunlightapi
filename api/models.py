from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField

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
    email = models.EmailField(blank=True)

    # other info
    gender = models.CharField(max_length=1, choices=GENDERS)

    # other site ids
    sunlight_old_id = models.CharField(max_length=20, blank=True)
    votesmart_id = models.CharField(max_length=20, blank=True)
    fec_id = models.CharField(max_length=20)
    crp_id = models.CharField(max_length=20)
    bioguide_id = models.CharField(max_length=20, primary_key=True)
    govtrack_id = models.CharField(max_length=20)
    eventful_id = models.CharField(max_length=20, blank=True)
    twitter_id = models.CharField(max_length=20, blank=True)
    congresspedia_url = models.URLField()

    def __unicode__(self):
        return '%s %s (%s-%s)' % (self.get_title_display(), self.lastname,
                                  self.party, self.state)

    class Meta:
        ordering = ('lastname', 'firstname')

class LegislatorBucket(models.Model):
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
    legislator = models.ForeignKey(Legislator)

    def get_legislator_name(self):
        if self.name_type == self.FIRST_LAST:
            return ' '.join([self.legislator.firstname, self.legislator.lastname])
        elif self.name_type == self.LAST_FIRST:
            return ' '.join([self.legislator.lastname, self.legislator.firstname])
        elif self.name_type == self.LAST:
            return self.legislator.lastname
        elif self.name_type == self.NICK_LAST:
            return ' '.join([self.legislator.nickname, self.legislator.lastname])
        elif self.name_type == self.LAST_NICK:
            return ' '.join([self.legislator.lastname, self.legislator.nickname])

    def __unicode__(self):
        return '%s is %s of %s' % (self.bucket, self.get_name_type_display(),
                                   self.legislator)

class ZipDistrict(models.Model):
    """ zip5 to district mapping """

    zip = models.CharField(max_length=5)
    state = models.CharField(max_length=2)
    district = models.CharField(max_length=10)

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
