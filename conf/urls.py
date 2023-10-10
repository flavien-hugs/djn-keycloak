from django.urls import path
from django.contrib import admin
from django.conf import settings

from account.routers import users_api


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/", users_api.urls),
]
