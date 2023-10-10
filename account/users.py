from typing import List

from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse

from ninja.pagination import paginate
from account.helpers import KeycloakAdminHelper, KeycloakOpenIDHelper


from commun.ninja import router_factory
from commun.utils import CustomPagination
from account.schema import (
    UserInSchema,
    UserLoginSchema,
    UserUpdateSchema,
)


User = get_user_model()

router = router_factory(tags=["users"])


@router.get("/@ping")
def ping(request):
    return {"msg": "healthy"}


@router.get("/", response=List[dict])
@paginate(CustomPagination)
def get_users(request: HttpRequest):
    kyc_admin = KeycloakAdminHelper()
    users_qs = kyc_admin.get_users_list()
    return users_qs


@router.post("/")
def create_user(request: HttpRequest, payload: UserInSchema):
    keycloak = KeycloakAdminHelper()
    return keycloak.create_user(
        email=payload.email,
        username=payload.email,
        firstname=payload.first_name,
        lastname=payload.last_name,
        password=payload.password,
    )


@router.post("/login", auth=None)
def login_user(request: HttpRequest, data: UserLoginSchema):
    kyc_openid = KeycloakOpenIDHelper()
    kyc_admin = KeycloakAdminHelper()

    ret = kyc_openid.login_user(data.email, data.password)
    id_user = ret["user_info"]["sub"]
    user = kyc_admin.get_user_detail(id_user)
    if "djn_users" in user.get("attributes", {}):
        return ret

    refresh_token = ret["token"]["refresh_token"]
    kyc_openid.logout_user(refresh_token)
    raise HttpResponse(status_code=403, detail="Forbidden")


@router.get("/{user_id}", auth=None)
def get_user(request: HttpRequest, user_id: str):
    kyc_admin = KeycloakAdminHelper()
    user = kyc_admin.get_user_detail(user_id)
    return 200, user


@router.patch("/{user_id}", auth=None)
def update_user(request: HttpRequest, user_id: str, payload: UserUpdateSchema):
    kyc_admin = KeycloakAdminHelper()
    _ = kyc_admin.update_user(user_id, payload.first_name, payload.last_name)
    user = kyc_admin.get_user_detail(user_id)
    return 200, user


@router.delete("/{user_id}", auth=None)
def delete_user(request: HttpRequest, user_id: str):
    kyc_admin = KeycloakAdminHelper()
    _ = kyc_admin.delete_user(user_id)
    return 204
