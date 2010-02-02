from django.contrib import admin
from sunlightapi.api.models import LogEntry

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'method', 'caller_key', 'output',
                    'error', 'query_string')
    list_display_links = ('timestamp',)
    list_filter = ('error','output')

admin.site.register(LogEntry, LogEntryAdmin)
