# Django settings for sunlight_api deployed

DEBUG = False

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

ADMIN_MEDIA_PREFIX = '/api/media/admin/'

LOCKSMITH_STATS_APP = 'congressapi'
TEMPLATE_DIRS = (
    '/home/api/lib/python/sunlightapi/templates/',
)

