from typing import List, Tuple

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse

from ninja.pagination import paginate
from account.helpers import KeycloakAdminHelper, KeycloakOpenIDHelper


from commun.ninja import router_factory
from commun.utils import CustomPagination
from account.schema import (
    UserInSchema,
    UserOutSchema,
    UserPatchSchema,
    UserLoginSchema,
)


User = get_user_model()

router = router_factory(tags=["users"])


@router.get("/@ping")
def ping(request):
    return {"msg": "healthy"}


@router.get("/", response=List[UserOutSchema])
@paginate(CustomPagination)
def get_users(request: HttpRequest):
    users_qs = User.objects.exclude(is_superuser=True)
    return users_qs


@router.post("/", response={201: UserOutSchema})
def create_user(request: HttpRequest, payload: UserInSchema):

    user_dict = payload.dict()
    user = User(**user_dict)
    user.set_password(payload.password)
    user.save()

    keycloak = KeycloakAdminHelper()
    return keycloak.create_user(
        email=payload.email,
        username=payload.email,
        firstname=payload.first_name,
        lastname=payload.last_name,
        password=payload.password
    )

@router.post("/login", auth=None)
def login_user(request: HttpRequest, data: UserLoginSchema):
    openid = KeycloakOpenIDHelper()
    kyc_admin = KeycloakAdminHelper()

    ret = openid.login_user(data.email, data.password)
    id_user = ret["user_info"]["sub"]
    user = kyc_admin.get_user_detail(id_user)
    if "djn_users" in user.get("attributes", {}):
        return ret

    refresh_token = ret["token"]["refresh_token"]
    openid.logout_user(refresh_token)
    raise HttpResponse(status_code=403, detail="Forbidden")


@router.get("/{user_id}", response={200: UserOutSchema})
def get_user(request: HttpRequest, user_id: int):
    user = get_object_or_404(User, id=user_id)
    return 200, user


@router.patch("/{user_id}", response={200: UserOutSchema})
def update_user(request: HttpRequest, user_id: int, payload: UserOutSchema):
    user = get_object_or_404(User, id=user_id)
    for attr, value in payload.dict().items():
        setattr(user, attr, value)
    user.save()
    return 200, user


@router.delete("/{user_id}", response={204: None})
def delete_user(request: HttpRequest, user_id: int):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return 204, None


@router.get("/logout")
def logout_user(request: HttpRequest):
    if request.user.is_anonymous is True:
        return 403, None
    logout(request)
    return 200, None
