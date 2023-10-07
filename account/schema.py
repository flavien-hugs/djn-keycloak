from django.contrib.auth import get_user_model

from ninja.orm import create_schema

User = get_user_model()


UserOutSchema = create_schema(
    User,
    name="UserOutSchema",
    exclude=['password', 'groups', 'user_permissions', 'is_superuser']
)

UserInSchema = create_schema(
    User,
    name="UserInSchema",
    fields=['first_name', 'last_name', 'email', 'password']
)

UserPatchSchema = create_schema(
    User,
    name="UserPatchSchema",
    fields=['first_name', 'last_name', 'email']
)

UserLoginSchema = create_schema(
    User,
    name="UserLoginSchema",
    fields=['email', 'password']
)
