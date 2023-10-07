from django.urls import path
from django.conf import settings
from django.contrib import admin


from account.api import users_api

urlpatterns = [
    path("api/", users_api.urls),
    path(settings.ADMIN_URL, admin.site.urls),
]
