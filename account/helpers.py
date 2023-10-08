import functools
from typing import Optional
from django.conf import settings

from keycloak import KeycloakOpenIDConnection, KeycloakAdmin, KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError


def refresh_keycloak_token(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except KeycloakAuthenticationError:
            self._init_keycloak_admin_connection()
            return func(self, *args, **kwargs)

    return wrapper


class KeycloakAdminHelper:
    def __init__(self):
        self._keycloak_admin = None

    def _init_keycloak_admin_connection(self):
        server_url = settings.AUTH_SERVER_ROOT + "/auth/"
        conn = KeycloakOpenIDConnection(
            server_url=server_url,
            username=settings.OIDC_RP_USERNAME,
            password=settings.OIDC_RP_PASSWORD,
            client_id=settings.OIDC_RP_CLIENT_ID,
            realm_name=settings.OIDC_RP_REALM_NAME,
            client_secret_key=settings.OIDC_RP_CLIENT_SECRET,
            verify=True,
        )
        self._keycloak_admin = KeycloakAdmin(connection=conn)

    def get_keycloak_admin_connection(self) -> KeycloakAdmin:
        if self._keycloak_admin is None:
            self._init_keycloak_admin_connection()
        return self._keycloak_admin

    @refresh_keycloak_token
    def get_users_list(self):
        users = self.get_keycloak_admin_connection().get_users({})
        return [user for user in users if "djn_users" in user.get("attributes", {})]


    @refresh_keycloak_token
    def get_user_detail(self, user_id: str):
        return self.get_keycloak_admin_connection().get_user(user_id)

    def create_user(
        self,
        email: str,
        username: str,
        password: str,
        firstname: Optional[str] = None,
        lastname: Optional[str] = None
    ):
        data = {
            "email": email,
            "username": username,
            "firstName": firstname,
            "lastName": lastname,
            "enabled": True,
            "emailVerified": True,
            "credentials": [{"type": "password", "value": password}],
            "attributes": {"locale": ["fr"], "djn_users": True},
        }
        new_user = self.get_keycloak_admin_connection().create_user(data, exist_ok=False)
        return self.get_keycloak_admin_connection().get_user(new_user)



class KeycloakOpenIDHelper:
    def __init__(self):
        self._keycloak_openid = None

    def _init_keycloak_openid_connection(self):
        server_url = settings.AUTH_SERVER_ROOT + "/auth/"
        self._keycloak_openid = KeycloakOpenID(
            server_url=server_url,
            client_id=settings.OIDC_RP_CLIENT_ID,
            realm_name=settings.OIDC_RP_REALM_NAME,
            client_secret_key=settings.OIDC_RP_CLIENT_SECRET,
            verify=True,
        )
        self._keycloak_openid.well_known()

    def get_keycloak_openid_connection(self) -> KeycloakOpenID:
        if self._keycloak_openid is None:
            self._init_keycloak_openid_connection()
        return self._keycloak_openid

    def login_user(self, username: str, password: str):
        openid = self.get_keycloak_openid_connection()
        token = openid.token(username=username, password=password)
        userinfo = openid.userinfo(token["access_token"])
        return {"token": token, "user_info": userinfo}

    def logout_user(self, refresh_token: str):
        return self.get_keycloak_openid_connection().logout(refresh_token)

