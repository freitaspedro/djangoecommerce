"""
Django settings for djangoecommerce project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '99999999999999999999999999999999999999999999999999')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

ADMINS = (
    ('Pedro', 'pvpfreitas@gmail.com'),
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'easy_thumbnails',
    'paypal.standard.ipn',
    'watson',
    'core',
    'catalog',
    'accounts',
    'checkout',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'checkout.middleware.cartitem_middleware',
]

ROOT_URLCONF = 'djangoecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # apps
                'catalog.context_processors.categories'
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# E-mail
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'admin@djangoecomerce.com'

# Auth
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_URL = 'logout'
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',
                            'accounts.backends.ModelBackend')

# Messages
from django.contrib.messages import constants
MESSAGE_TAGS = {
    constants.DEBUG: 'debug',
    constants.INFO: 'info',
    constants.SUCCESS: 'success',
    constants.WARNING: 'warning',
    constants.ERROR: 'danger',
}

PAGSEGURO_TOKEN = ''
PAGSEGURO_EMAIL = 'admin@djangoecomerce.com'
PAGSEGURO_SANDBOX = True

PAYPAL_EMAIL = 'admin@djangoecomerce.com'
PAYPAL_TEST = True

# AWS
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

AWS_S3_SECURE_URLS = True
AWS_QUERYSTRING_AUTH = False
AWS_PRELOAD_METADATA = True
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = 'app-django-ecommerce'
AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME

STATICFILES_STORAGE = 'djangoecommerce.s3util.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

DEFAULT_FILE_STORAGE = 'djangoecommerce.s3util.MediaStorage'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

AWS_HEADERS = {
    'x-amz-acl': 'public-read',
    'Cache-Control': 'public, max-age=31556926'
}

# Thumbnails
THUMBNAIL_ALIASES = {
    '': {
        'product_image': {'size': (285, 160), 'crop': True},
    },
}

THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
    }
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'checkout.views': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'filename': os.path.join(BASE_DIR, 'checkout.views.log'),
        }
    },
    'loggers': {
        'checkout.views': {
            'handlers': ['checkout.views'],
            'level': 'DEBUG',
        }
    }
}


try:
    from .local_settings import *
except ImportError:
    pass
