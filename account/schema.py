from ninja.orm import create_schema
from account.models import CustomUser



UserOutSchema = create_schema(
    CustomUser,
    name="UserOutSchema",
    exclude=['password', 'groups', 'user_permissions', 'is_superuser']
)

UserInSchema = create_schema(
    CustomUser,
    name="UserInSchema",
    fields=['first_name', 'last_name', 'email', 'password']
)

UserPatchSchema = create_schema(
    CustomUser,
    name="UserPatchSchema",
    fields=['first_name', 'last_name', 'email']
)

UserLoginSchema = create_schema(
    CustomUser,
    name="UserLoginSchema",
    fields=['email', 'password']
)
