# Django settings for annotation project.
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
import os,sys
#HERE=os.path.dirname(os.path.abspath(__file__))
# import os.path
# reload(sys)
# sys.setdefaultencoding('utf-8')
# gettext = lambda s: s

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

HERE=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if HERE not in sys.path:
    sys.path.insert(1,HERE)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
# ALLOWED_HOSTS='127.0.0.1'
# MANAGERS = ADMINS
#
# if 'SERVER_SOFTWARE' in os.environ:
#     from bae.core import const
#     DATABASES={
#         'default':{
#             'ENGINE':'django.db.backends.mysql',
#             'NAME':'HigpKaEEFBDIfjDHpvou',
#             'USER':const.MYSQL_USER,
#             'PASSWORD':const.MYSQL_PASS,
#             'HOST':const.MYSQL_HOST,
#             'PORT':const.MYSQL_PORT,
#         }
#     }
# else:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pr_site',
        'USER': 'david',
        'PASSWORD': 'david',
        'HOST': 'localhost',
        'PORT': '',
    }
}
# DATABASES = {
#      'default': {
#            'ENGINE': 'django.db.backends.sqlite3',
#            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#      }
#   }
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
# TIME_ZONE='Asia/Shanghai'
LANGUAGE_CODE = 'en-us'


FILE_CHARSET='UTF-8'
DEFAULT_CHARSET='utf-8'
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(HERE,'media').replace('\\','/')+'/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(HERE,'static').replace('\\','/')+'/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ("css", os.path.join(STATIC_ROOT,'css')),
    ("js", os.path.join(STATIC_ROOT,'js')),
    ("images", os.path.join(STATIC_ROOT,'images')),
    ("bootstrap",os.path.join(STATIC_ROOT,'bootstrap')),
    ("assets",os.path.join(STATIC_ROOT,'assets')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'y#%hu*w4d9*^kh6&amp;=0kvjz=bxf&amp;-#l3#w9r8=hus1rjsdzvjnb'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#   'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = ( 'django.core.context_processors.static',
                                'django.core.context_processors.media',
                                'django.contrib.auth.context_processors.auth',
                                'django.core.context_processors.request',    )

#
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

  #  'apps.main.middleware.AjaxMessaging',
  # Uncomment the next line for simple clickjacking protection:
  # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'annotation.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'annotation.wsgi.application'



# TEMPLATE_DIRS =(
#     # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.
# )

# AUTH_PROFILE_MODULE = 'markpic.UserProfile'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    #'endless_pagination',

    'xadmin',
    'crispy_forms',
    'reversion',
    'markpic',

)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTH_PROFILE_MODULE='markpic.UserProfile'
