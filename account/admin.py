import uuid

from django.contrib import admin

from account.models import CustomUser
from account.helpers import KeycloakAdminHelper


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    exclude = ["keycloak_uuid", "date_joined", "password"]
    keycloak_connection = KeycloakAdminHelper()

    def save_model(self, request, obj, form, change):
        if not change:
            super().save_model(request, obj, form, change)

            keycloak_id = self.keycloak_connection.create_user(
                obj.email, obj.email
            )
            obj.keycloak_uuid = keycloak_id
        super().save_model(request, obj, form, change)
