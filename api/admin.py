from django.contrib import admin
from sunlightapi.api.models import ApiUser, LogEntry

class ApiUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'key', 'status', 'org_name', 'org_url',
                    'usage', 'issued_on')
    list_display_links = ('email', 'key')
    list_filter = ('status',)

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'method', 'caller_key', 'output',
                    'error', 'query_string')
    list_display_links = ('timestamp',)
    list_filter = ('error','output')

admin.site.register(ApiUser, ApiUserAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
