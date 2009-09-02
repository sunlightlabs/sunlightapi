import os
from django.contrib.gis.utils import LayerMapping
from sunlightapi.districts.models import CongressDistrict

cd_mapping = {
    'state_fips': 'STATE',
    'district': 'CD',
    'mpoly': 'MULTIPOLYGON',
}

cd_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'congdist/cd99_110.shp'))

# Mapping of FIPS codes to Postal Abbreviations
# obtained from http://www.itl.nist.gov/fipspubs/fip5-2.htm
FIPS_TO_STATE = {
    '01':'AL', '02':'AK', '04':'AZ', '05':'AR', '06':'CA', '08':'CO', '09':'CT',
    '10':'DE', '11':'DC', '12':'FL', '13':'GA', '15':'HI', '16':'ID', '17':'IL',
    '18':'IN', '19':'IA', '20':'KS', '21':'KY', '22':'LA', '23':'ME', '24':'MD',
    '25':'MA', '26':'MI', '27':'MN', '28':'MS', '29':'MO', '30':'MT', '31':'NE',
    '32':'NV', '33':'NH', '34':'NJ', '35':'NM', '36':'NY', '37':'NC', '38':'ND',
    '39':'OH', '40':'OK', '41':'OR', '42':'PA', '44':'RI', '45':'SC', '46':'SD',
    '47':'TN', '48':'TX', '49':'UT', '50':'VT', '51':'VA', '53':'WA', '54':'WV',
    '55':'WI', '56':'WY', '72':'PR' }

def run(verbose=True):
    lm = LayerMapping(CongressDistrict, cd_shp, cd_mapping, transform=False,
                      encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)

    for cd in CongressDistrict.objects.all():
        cd.state_abbrev = FIPS_TO_STATE[cd.state_fips]
        cd.save()

