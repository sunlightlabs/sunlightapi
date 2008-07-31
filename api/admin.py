from django.contrib import admin
from sunlightapi.api.models import Legislator, Method, Source

class LegislatorAdmin(admin.ModelAdmin):
    list_display = ('title', 'firstname', 'lastname', 'party', 'state',
                    'district')
    list_display_links = ('firstname', 'lastname')

admin.site.register(Legislator, LegislatorAdmin)
admin.site.register(Method)
admin.site.register(Source)
