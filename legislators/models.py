from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
from sunlightapi.api.models import NameMatchingBucket

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

class LegislatorBucket(NameMatchingBucket):
    person = models.ForeignKey(Legislator)

CHAMBERS = (('House', 'House'),('Senate','Senate'))

class Committee(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    chamber = models.CharField(max_length=6, choices=CHAMBERS)
    parent = models.ForeignKey('self', related_name='subcommittees', null=True)
    name = models.CharField(max_length=300)
    members = models.ManyToManyField(Legislator, related_name='committees')

    def __unicode__(self):
        return self.name
