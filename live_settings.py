# Django settings for sunlight_api deployed

from settings import *

DEBUG = False

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'sunlightapi'
DATABASE_USER = 'sunlightapi'
DATABASE_PASSWORD = '***REMOVED***'
DATABASE_HOST = 'services.sunlightlabs.com'
DATABASE_PORT = ''

ADMIN_MEDIA_PREFIX = '/api/media/admin/'


TEMPLATE_DIRS = (
    '/home/admin/django-projects/sunlightapi/templates/',
)

