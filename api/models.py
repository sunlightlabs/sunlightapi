from django.db import models

# choices for party
PARTIES = (
    ('D', 'Democrat'),
    ('I', 'Independent'),
    ('R', 'Republican'))

# short and long form of titles
TITLES = (
    ('Rep', 'Representative'),
    ('Sen', 'Senator'))

# short and long form of genders
GENDERS = (
    ('F', 'Female'),
    ('M', 'Male'))

class Legislator(models.Model):
    """ Model containing basic information for legislators """

    # name
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30)
    name_suffix = models.CharField(max_length=5, blank=True)
    nickname = models.CharField(max_length=30, blank=True)

    # job
    title = models.CharField(max_length=3, choices=TITLES)
    state = models.CharField(max_length=2)
    district = models.CharField(max_length=12, blank=True)
    party = models.CharField(max_length=1, choices=PARTIES)

    # contact info
    congress_office = models.CharField(max_length=50)
    phone = models.PhoneNumberField()
    fax = models.PhoneNumberField()
    website = models.URLField()
    webform = models.URLField(blank=True)
    email = models.EmailField(blank=True)

    # other info
    gender = models.CharField(max_length=1, choices=GENDERS)

    # other site ids
    sunlight_old_id = models.CharField(max_length=20, blank=True)
    votesmart_id = models.CharField(max_length=20)
    fec_id = models.CharField(max_length=20)
    crp_id = models.CharField(max_length=20)
    bioguide_id = models.CharField(max_length=20, primary_key=True)
    govtrack_id = models.CharField(max_length=20)
    eventful_id = models.CharField(max_length=20, blank=True)
    congresspedia_url = models.URLField()

    def __unicode__(self):
        return '%s %s (%s-%s)' % (self.get_title_display(), self.lastname,
                                  self.party, self.state)

    class Meta:
        ordering = ('lastname', 'firstname')

# show Legislator in databrowse app
#from django.contrib import databrowse
#databrowse.site.register(Legislator)

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
