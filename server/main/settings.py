"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
import os
import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v7cl8h-1inc531fjm5-@f&la76rjy&)ldsdbmptxu8zyyj=kk1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
CORS_ORIGIN_ALLOW_ALL=True


# Postgres
DB_HOST = env.str('DB_HOST')
DB_NAME = env.str('DB_NAME')
DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')

# Google Sheet
SPREAD_SHEET_ID = env.str('SPREAD_SHEET_ID')
SHEET_ID = env.str('SHEET_ID')
GOOGLE_SHEET_NAME = env.str('GOOGLE_SHEET_NAME')
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'main', 'credentials.json')
JOB_URL_COLUMN_INDEX = 13
LOCK_COLUMN_INDEX = 27
STARTED_AT_COLUMN_INDEX = 28
APPLIED_FOR_DATE_COLUMN_INDEX = 17
PROBLEM_APPLYING_COLUMN_INDEX = 32

# OpenAI API Key
OPENAI_API_KEY = env.str('OPENAI_API_KEY')

# Azure AD Configuration
AZURE_AD_OAUTH2_KEY = env.str('AZURE_AD_OAUTH2_KEY')
AZURE_AD_OAUTH2_SECRET = env.str('AZURE_AD_OAUTH2_SECRET')
AZURE_AD_OAUTH2_TENANT_ID = env.str('AZURE_AD_OAUTH2_TENANT_ID')

# Redirect URI (same as in Azure AD configuration)
LOGIN_REDIRECT_URL = env.str('LOGIN_REDIRECT_URL')
LOGIN_ERROR_URL = '/login-error/'
REDIRECT_IS_HTTPS = True

AZURE_AD_AUTH_URL = f'https://login.microsoftonline.com/{AZURE_AD_OAUTH2_TENANT_ID}/oauth2/v2.0/authorize'
AZURE_AD_TOKEN_URL = f'https://login.microsoftonline.com/{AZURE_AD_OAUTH2_TENANT_ID}/oauth2/v2.0/token'

# Scraper Run Status
SCRAPER_RUN_STATUS = {
    'READY': 'READY',
    'RUNNING': 'RUNNING',
    'SUCCEEDED': 'SUCCEEDED',
    'FAILED': 'FAILED',
    'TIMED_OUT': 'TIMED_OUT',
    'ABORTED': 'ABORTED',
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'corsheaders',
    'job',
    'scraper',
    'setting',
    'resume',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '5432',
    }
}


# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'social_core.backends.azuread.AzureADOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
