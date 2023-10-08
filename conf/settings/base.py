import os

from pathlib import Path

from dotenv import dotenv_values

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(os.path.dirname(abspath))
BASE_DIR = os.path.dirname(dirname)

appenv = dotenv_values("./secrets/djn.env")
kycenv = dotenv_values("./secrets/keycloak.env")


SECRET_KEY = appenv.get("SECRET_KEY")

DEBUG = appenv.get("DEBUG")
ALLOWED_HOSTS = ["*"]
ADMIN_URL = appenv.get("ADMIN_URL")
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

DJANGO_SETTINGS_MODULE = appenv.get("DJANGO_SETTINGS_MODULE")
NINJA_PAGINATION_PER_PAGE = 10

OIDC_RP_USERNAME = kycenv.get("KEYCLOAK_USER")
OIDC_RP_PASSWORD = kycenv.get("KEYCLOAK_PASSWORD")
AUTH_SERVER_ROOT = kycenv.get("KEYCLOAK_SERVER_URL")
OIDC_RP_REALM_NAME = kycenv.get("KEYCLOAK_REALM_NAME")
OIDC_RP_CLIENT_ID = kycenv.get("KEYCLOAK_REALM_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = kycenv.get("KEYCLOAK_REALM_SECRET_KEY")
