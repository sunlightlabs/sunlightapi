# Django settings for sunlight_api deployed

DEBUG = False

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'sunlightapi'
DATABASE_USER = 'sunlightapi'
DATABASE_PASSWORD = '***REMOVED***'
DATABASE_HOST = 'morgan.int'
DATABASE_PORT = ''

ADMIN_MEDIA_PREFIX = '/api/media/admin/'


TEMPLATE_DIRS = (
    '/home/api/lib/python/sunlightapi/templates/',
)

