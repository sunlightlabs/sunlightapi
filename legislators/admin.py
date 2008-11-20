from django.contrib import admin
from sunlightapi.legislators.models import Legislator

class LegislatorAdmin(admin.ModelAdmin):
    list_display = ('title', 'firstname', 'lastname', 'party', 'state',
                    'district')
    list_display_links = ('firstname', 'lastname')
    
admin.site.register(Legislator, LegislatorAdmin)