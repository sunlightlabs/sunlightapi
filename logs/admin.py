from django.contrib import admin
from sunlightapi.logs.models import ApiUser, LogEntry

class ApiUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'api_key', 'status', 'org_name', 'org_url',
                    'usage', 'signup_time')
    list_display_links = ('email', 'api_key')
    list_filter = ('status',)

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'method', 'caller_key', 'output',
                    'error', 'query_string')
    list_display_links = ('timestamp',)
    list_filter = ('error','output')

admin.site.register(ApiUser, ApiUserAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
