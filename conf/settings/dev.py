import os
from . import *  # noqa F405

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(os.path.dirname(abspath))
BASE_DIR = os.path.dirname(dirname)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
