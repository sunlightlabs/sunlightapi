from django.db import models

PARTIES = (
    ('D', 'Democrat'),
    ('I', 'Independent'),
    ('R', 'Republican'))

TITLES = (
    ('Rep', 'Representative'),
    ('Sen', 'Senator'))

GENDERS = (
    ('F', 'Female'),
    ('M', 'Male'))

class Legislator(models.Model):
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30)
    name_suffix = models.CharField(max_length=5, blank=True)
    nickname = models.CharField(max_length=30, blank=True)

    title = models.CharField(max_length=3, choices=TITLES)
    state = models.CharField(max_length=2)
    district = models.CharField(max_length=10, blank=True)
    party = models.CharField(max_length=1, choices=PARTIES)

    congress_office = models.CharField(max_length=50)
    phone = models.PhoneNumberField()
    fax = models.PhoneNumberField()
    website = models.URLField()
    webform = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS)

    # other site ids
    sunlight_old_id = models.CharField(max_length=20)
    votesmart_id = models.CharField(max_length=20)
    fec_id = models.CharField(max_length=20)
    crp_id = models.CharField(max_length=20)
    bioguide_id = models.CharField(max_length=20)
    govtrack_id = models.CharField(max_length=20)
    eventful_id = models.CharField(max_length=20)
    congresspedia_url = models.URLField()

    def __unicode__(self):
        return '%s %s (%s-%s)' % (self.get_title_display(), self.lastname,
                                  self.party, self.state)

    class Admin:
        pass

class ZipDistrict(models.Model):
    zip = models.CharField(max_length=5)
    state = models.CharField(max_length=2)
    district = models.CharField(max_length=10)

from django.contrib import databrowse
databrowse.site.register(Legislator)

class Method(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

class Source(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    last_update = models.DateField()
    source_for = models.ManyToManyField(Method)

    def __unicode__(self):
        return '%s [updated %s]' % (self.name, self.last_update)

    class Admin:
        pass
