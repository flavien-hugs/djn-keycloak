import functools
from typing import Optional
from django.conf import settings

from keycloak import KeycloakAdmin
from keycloak.exceptions import KeycloakAuthenticationError


def refresh_keycloak_token(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except KeycloakAuthenticationError:
            self._init_keycloak_connection()
            return func(self, *args, **kwargs)

    return wrapper


class KeycloakHelper:
    def __init__(self):
        self._keycloak_admin = None

    def _init_keycloak_connection(self):
        server_url = settings.AUTH_SERVER_ROOT + "/auth/"
        self._keycloak_admin = KeycloakAdmin(
            server_url=server_url,
            client_id=settings.OIDC_RP_CLIENT_ID,
            realm_name=settings.OIDC_RP_REALM_NAME,
            client_secret_key=settings.OIDC_RP_CLIENT_SECRET,
            verify=True,
        )

    def get_keycloak_connection(self) -> KeycloakAdmin:
        """
        Wrapper to get the keycloak connection.
        Performs lazy initialization of the keycloak connection.
        """
        if self._keycloak_admin is None:
            self._init_keycloak_connection()
        return self._keycloak_admin

    @refresh_keycloak_token
    def get_user_detail(self, user_id: str):
        return self.get_user(user_id)

    @refresh_keycloak_token
    def create_user(
        self,
        email: str,
        password: str
    ):
        payload = {
            "email": email,
            "enabled": True,
            "credentials": [{"type": "password", "value": password}],
        }
        return self.get_keycloak_connection().create_user(payload)
