
import os
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings.DJANGO_SETTINGS_MODULE)

if os.getenv("DJANGO_SETTINGS_MODULE"):
    os.environ["DJANGO_SETTINGS_MODULE"] = settings.DJANGO_SETTINGS_MODULE

application = get_wsgi_application()
