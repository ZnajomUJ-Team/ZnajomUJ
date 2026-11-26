from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


def normalize_email(email):
    """Return the e-mail address trimmed and lowercased, so it is unique regardless of case."""
    return (email or "").strip().lower()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = normalize_email(email)
        if not email:
            raise ValueError("Adres e-mail jest wymagany.")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superużytkownik musi mieć is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superużytkownik musi mieć is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        # Logowanie nie zależy od wielkości liter w adresie e-mail.
        return self.get(email__iexact=normalize_email(email))


class User(AbstractBaseUser, PermissionsMixin):
    """Konto uczestnika. Logowanie adresem e-mail, bez nazwy użytkownika.

    Dane profilu (imię, nazwisko, płeć, data urodzenia, wydział) dochodzą w T18.
    """

    email = models.EmailField(
        "adres e-mail",
        unique=True,
        error_messages={"unique": "Konto z tym adresem e-mail już istnieje."},
    )
    is_staff = models.BooleanField(
        "dostęp do panelu",
        default=False,
        help_text="Czy użytkownik może logować się do panelu administracyjnego.",
    )
    is_active = models.BooleanField(
        "aktywne",
        default=False,
        help_text="Konto staje się aktywne po potwierdzeniu adresu e-mail (T14).",
    )
    date_joined = models.DateTimeField("data rejestracji", default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "użytkownik"
        verbose_name_plural = "użytkownicy"

    def clean(self):
        super().clean()
        self.email = normalize_email(self.email)

    def save(self, *args, **kwargs):
        self.email = normalize_email(self.email)
        super().save(*args, **kwargs)
