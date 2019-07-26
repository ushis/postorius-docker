# -*- coding: utf-8 -*-
# Copyright (C) 1998-2016 by the Free Software Foundation, Inc.
#
# This file is part of Postorius.
#
# Postorius is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Postorius is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# Postorius.  If not, see <http://www.gnu.org/licenses/>.

"""
Django settings for postorius project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('POSTORIUS_SECRET_KEY', '3d2b4a5a760e7a4d73d526f4eaeb05a3')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('POSTORIUS_DEBUG', '') == 'True'

# Define admins like so:
# export POSTORIUS_ADMINS='admin:admin@example.org admin2:admin2@example.org'
ADMINS = tuple([tuple(adm.split(':')) for adm in os.getenv('POSTORIUS_ADMINS', '').split()])

ALLOWED_HOSTS = os.getenv('POSTORIUS_ALLOWED_HOSTS', 'localhost:8000').split()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Mailman API credentials
MAILMAN_REST_API_URL = os.getenv('MAILMAN_API_URL', 'http://mailman:8001')
MAILMAN_REST_API_USER = os.getenv('MAILMAN_API_USER', 'admin')
MAILMAN_REST_API_PASS = os.getenv('MAILMAN_API_PASS', 'secret')

# Application definition
INSTALLED_APPS = (
    'django_gravatar',
    'django_mailman3',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'postorius',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'postorius.middleware.PostoriusMiddleware',
)

# Set `postorius.urls` as main url config if Postorius
# is the only app you want to serve.
ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.csrf',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_mailman3.context_processors.common',
                'postorius.context_processors.postorius',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB', 'postorius'),
        'USER': os.getenv('POSTGRES_USER', 'postorius'),
        'PASSWORD': os.getenv('POSTGRES_PASS', 'secret'),
        'HOST': os.getenv('POSTGRES_HOST', 'postgres'),
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.getenv('POSTORIUS_TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'list_index'
LOGOUT_URL = 'account_logout'

# Compatibility with Bootstrap 3
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_UNIQUE_EMAIL = True

# From Address for emails sent to users
DEFAULT_FROM_EMAIL = os.getenv('POSTORIUS_FROM_EMAIL', 'postorius@localhost.local')
# From Address for emails sent to admins
SERVER_EMAIL = os.getenv('POSTORIUS_SERVER_EMAIL', 'root@localhost.local')

# These can be set to override the defaults but are not mandatory:
# EMAIL_CONFIRMATION_TEMPLATE = 'postorius/address_confirmation_message.txt'
# EMAIL_CONFIRMATION_SUBJECT = 'Confirmation needed'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('POSTORIUS_EMAIL_HOST', 'localhost')
EMAIL_PORT = os.getenv('POSTORIUS_EMAIL_PORT', '25')

# You can enable logging by uncommenting the following lines
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
