# Django settings for sunlight_api deployed

DEBUG = True
TEMPLATE_DEBUG = DEBUG
if DEBUG:
    CACHE_BACKEND = 'dummy:///'
else:
    CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

ADMINS = (
    ('James Turk', 'james.p.turk@gmail.com'),
)
MANAGERS = ADMINS
EMAIL_SUBJECT_PREFIX = '[Sunlight API]'

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'sunlightapi'
DATABASE_USER = 'sunlightapi'
DATABASE_PASSWORD = '***REMOVED***'
DATABASE_HOST = 'services.sunlightlabs.com'
DATABASE_PORT = ''

EMAIL_HOST = 'mail.sunlightfoundation.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'bounce@sunlightfoundation.com'
EMAIL_HOST_PASSWORD = 'b0unc3'
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL=EMAIL_HOST_USER

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/api/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '***REMOVED***'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'sunlightapi.urls'

TEMPLATE_DIRS = (
    '/home/admin/django-projects/sunlightapi/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.databrowse',
    'django.contrib.flatpages',
    'sunlightapi.api',
    'sunlightapi.logs',
    'django-sunlightcore',
)
