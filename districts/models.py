from django.db import models

class ZipDistrict(models.Model):
    """ zip5 to district mapping """

    zip = models.CharField(max_length=5)
    state = models.CharField(max_length=2)
    district = models.CharField(max_length=10)