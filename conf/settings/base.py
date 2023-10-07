import os

from pathlib import Path

from dotenv import dotenv_values

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(os.path.dirname(abspath))
BASE_DIR = os.path.dirname(dirname)

env = dotenv_values("./secrets/app.djn.env")


SECRET_KEY = env.get("SECRET_KEY")

DEBUG = env.get("DEBUG")
ALLOWED_HOSTS = ["*"]
ADMIN_URL = env.get("ADMIN_URL")
AUTH_USER_MODEL = "account.CustomUser"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = ["account.apps.AccountConfig"]

INSTALLED_APPS += LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


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

USE_TZ = False
TIME_ZONE = "UTC"
LANGUAGE_CODE = "fr"
USE_I18N = USE_L10N = True
LANGUAGE_COOKIE_SECURE = True

STATIC_URL = 'static/'
DATETIME_FORMAT = "l F o"
DATE_INPUT_FORMATS = ("%d/%m/%Y", "%d-%m-%Y")
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJANGO_SETTINGS_MODULE = env.get("DJANGO_SETTINGS_MODULE")
NINJA_PAGINATION_PER_PAGE = 10

AUTH_SERVER_ROOT = env.get("KEYCLOAK_SERVER_URL")
OIDC_RP_CLIENT_ID = env.get("KEYCLOAK_ADMIN_CLIENT_ID")
OIDC_RP_REALM_NAME = env.get("KEYCLOAK_ADMIN_REALM_NAME")
OIDC_RP_CLIENT_SECRET = env.get("KEYCLOAK_ADMIN_SECRET_KEY")
