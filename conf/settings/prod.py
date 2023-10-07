import os

from .base import *  # noqa F405
from dotenv import dotenv_values

env = dotenv_values("./secrets/app.djn.env")

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(os.path.dirname(abspath))
BASE_DIR = os.path.dirname(dirname)

APPEND_SLASH = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.get("POSTGRES_DB"),
        "USER": env.get("POSTGRES_USER"),
        "PASSWORD": env.get("POSTGRES_PASSWORD"),
        "HOST": env.get("POSTGRES_HOST"),
        "PORT": env.get("POSTGRES_PORT"),
        "ATOMIC_REQUESTS": True,
    }
}

SECURE_HSTS_SECONDS = 86400
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CSRF_USE_SESSIONS = True
CSRF_COOKIE_SECURE = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/debug.log"),
            "when": "D",
            "interval": 1,
            "backupCount": 100,
        },
    },
    "loggers": {
        "django": {"handlers": ["file"], "level": "INFO", "propagate": True},
        "project": {"handlers": ["file"], "level": "INFO", "propagate": True},
        "": {"handlers": ["file"], "level": "INFO", "propagate": True},
    },
}
