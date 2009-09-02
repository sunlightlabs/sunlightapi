from django.contrib.gis.db import models

class ZipDistrict(models.Model):
    """ zip5 to district mapping """

    zip = models.CharField(max_length=5)
    state = models.CharField(max_length=2)
    district = models.CharField(max_length=10)

class CongressDistrict(models.Model):
    state_abbrev = models.CharField(max_length=2)
    state_fips = models.CharField(max_length=2)
    district = models.CharField(max_length=2)

    mpoly = models.MultiPolygonField()
    objects = models.GeoManager()

    def __unicode__(self):
        return '%s-%s' % (self.state_abbrev, self.district)

