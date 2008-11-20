from django.db import models

class Filing(models.Model):
    filing_id = models.CharField(max_length=36, primary_key=True)
    filing_period = models.CharField(max_length=30)
    filing_date = models.DateField()
    filing_amount = models.IntegerField(null=True)
    filing_year = models.IntegerField()
    filing_type = models.CharField(max_length=30)
    
    # client is optional
    client_senate_id = models.IntegerField(null=True)
    client_name = models.CharField(max_length=100, null=True)
    client_country = models.CharField(max_length=30, null=True)
    client_state = models.CharField(max_length=30, null=True)
    client_ppb_country = models.CharField(max_length=30, null=True)
    client_ppb_state = models.CharField(max_length=30, null=True)
    client_description = models.CharField(max_length=200, null=True)
    client_firstname = models.CharField(max_length=30, null=True)
    client_middlename =  models.CharField(max_length=30, null=True)
    client_lastname = models.CharField(max_length=30, null=True)
    client_suffix = models.CharField(max_length=4, null=True)
    client_raw_contact_name = models.CharField(max_length=100, null=True)
    
    registrant_senate_id = models.IntegerField(null=True)
    registrant_name = models.CharField(max_length=50, null=True)
    registrant_firstname = models.CharField(max_length=30, null=True)
    registrant_middlename =  models.CharField(max_length=30, null=True)
    registrant_lastname = models.CharField(max_length=30, null=True)
    registrant_suffix = models.CharField(max_length=4, null=True)
    registrant_raw_name = models.CharField(max_length=100, null=True)
    registrant_description = models.CharField(max_length=100, null=True)
    registrant_address = models.CharField(max_length=100, null=True)
    registrant_country = models.CharField(max_length=30, null=True)
    registrant_ppb_country = models.CharField(max_length=30, null=True)
    
    def __unicode__(self):
        return '%s (%s/%s)' % (self.filing_id, self.registrant_name, self.client_name)
    
    def to_dict(self):
        fdict = dict(self.__dict__)
        fdict['issues'] = [i.to_dict() for i in self.issues.all()]
        fdict['lobbyists'] = [l.to_dict() for l in self.lobbyists.all()]
        return {'filing': fdict}
    
    def sopr_url(self):
        return 'http://soprweb.senate.gov/index.cfm?event=getFilingDetails&filingID=%s' % self.filing_id


class Issue(models.Model):
    code = models.CharField(max_length=100)
    specific_issue = models.CharField(max_length=100)
    
    filing = models.ForeignKey(Filing, related_name='issues')
    
    def __unicode__(self):
        return '%s: %s' % (self.code, self.specific_issue)
    
    def to_dict(self):
        idict = dict(self.__dict__)
        idict.pop('id')
        idict.pop('filing_id')
        return {'issue': idict}
    
class Lobbyist(models.Model):
    firstname = models.CharField(max_length=30)
    middlename =  models.CharField(max_length=30, null=True)
    lastname = models.CharField(max_length=30)
    suffix = models.CharField(max_length=4, null=True)
    official_position = models.CharField(max_length=50)
    raw_name = models.CharField(max_length=100, null=True)
    
    filing = models.ForeignKey(Filing, related_name='lobbyists')
    
    def __unicode__(self):
        return '%s %s' % (self.firstname, self.lastname)
    
    def to_dict(self):
        ldict = dict(self.__dict__)
        ldict.pop('id')
        ldict.pop('filing_id')
        return {'lobbyist': ldict}