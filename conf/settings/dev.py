import os
from .base import *  # noqa F405

from dotenv import dotenv_values

env = dotenv_values("./secrets/db.env")


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
