from typing import List, Tuple

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, logout, login

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse

from ninja.pagination import paginate


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
    return 201, user


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


@router.post("/login", response=UserOutSchema, auth=None)
def login_user(request: HttpRequest, data: UserLoginSchema):
    form = AuthenticationForm(data=data.dict())
    user = authenticate(
        username=form.cleaned_data.get("username"),
        password=form.cleaned_data.get("password"),
    )
    if user is not None:
        login(request, user)
        return JsonResponse(status_code=200, content="Login success")
    else:
        return JsonResponse(status_code=401, content="Login refuse")
