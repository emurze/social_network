import datetime
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = bool(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = ['mysite.com', '0.0.0.0', '127.0.0.1', '192.168.100.7']

INSTALLED_APPS = [
    'apps.registration.apps.RegistrationConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.humanize',
    'django.forms',
    'debug_toolbar',
    'easy_thumbnails',
    'rest_framework',

    'apps.base.apps.BaseConfig',
    'apps.account.apps.AccountConfig',
    'apps.post.apps.PostConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

APPS_DIR = BASE_DIR / 'apps'

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    *APPS_DIR.rglob('*static'),
]
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [*APPS_DIR.rglob('*templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_ADMIN_NAME = 'adm1'
DEFAULT_ADMIN_PASSWORD = 'adm1'
DEFAULT_ADMIN_EMAIL = 'adm1@adm1.com'

LOGOUT_URL = 'logout'
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

START_REQUEST_POST_COUNT = 8
REQUEST_POST_COUNT = 14

REQUEST_REPLY_COUNT = 8

DEFAULT_USER_COUNT = 15
REQUEST_USER_COUNT = 30

DEFAULT_SHOWED_FOLLOWINGS_PAGE = 1
DEFAULT_FOLLOWINGS_COUNT = 8
REQUEST_FOLLOWINGS_COUNT = 8

OLDEST_HUMAN = 122
CURRENT_YEAR = datetime.date.today().year

# if DEBUG:
#     import socket  # only if you haven't already imported this
#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + \
#                    ["0.0.0.0", "127.0.0.1", "10.0.2.2"]
#     MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
