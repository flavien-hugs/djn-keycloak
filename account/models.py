import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from commun.models import BaseTimeStampModel
from account.managers import CustomUserManager


class CustomUser(AbstractUser, PermissionsMixin, BaseTimeStampModel):

    username = None

    keycloak_uuid = models.UUIDField(
        editable=False, unique=True,
        default=uuid.uuid4
    )
    email = models.EmailField(
        unique=True,
        max_length=180,
        verbose_name="address email",
        error_messages={"unique": "This email is already in use"},
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ["-date_joined", "-last_login"]
        verbose_name = "Utilisateurs"
        verbose_name_plural = verbose_name
        indexes = [models.Index(fields=["id"])]

    def __str__(self) -> str:
        string = self.email if self.email != "" else self.get_full_name()
        return string
