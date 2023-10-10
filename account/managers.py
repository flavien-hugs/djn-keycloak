from django.utils import timezone
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, **extra_fields):

        if email is None:
            raise TypeError("L'adresse e-mail est requise !")

        if password is None:
            raise TypeError("Le mot de passe est requis !")

        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email, last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)
