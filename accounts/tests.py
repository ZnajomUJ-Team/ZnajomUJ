from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import FieldDoesNotExist
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import User

PASSWORD = "Bezpieczne-haslo-123"


class UserModelTests(TestCase):
    def test_project_uses_custom_user_model(self):
        self.assertIs(get_user_model(), User)

    def test_user_has_no_username_field(self):
        with self.assertRaises(FieldDoesNotExist):
            User._meta.get_field("username")

    def test_create_user(self):
        user = User.objects.create_user(email="jan.kowalski@student.uj.edu.pl", password=PASSWORD)
        self.assertEqual(user.email, "jan.kowalski@student.uj.edu.pl")
        self.assertEqual(user.get_username(), user.email)
        self.assertEqual(str(user), user.email)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_new_user_is_inactive_until_email_confirmed(self):
        user = User.objects.create_user(email="jan@student.uj.edu.pl", password=PASSWORD)
        self.assertFalse(user.is_active)

    def test_email_is_lowercased_and_trimmed(self):
        user = User.objects.create_user(email="  Jan.Kowalski@STUDENT.UJ.EDU.PL ", password=PASSWORD)
        self.assertEqual(user.email, "jan.kowalski@student.uj.edu.pl")

    def test_email_is_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password=PASSWORD)

    def test_email_is_unique_regardless_of_case(self):
        User.objects.create_user(email="jan@student.uj.edu.pl", password=PASSWORD)
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="JAN@student.uj.edu.pl", password=PASSWORD)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(email="admin@student.uj.edu.pl", password=PASSWORD)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

    def test_superuser_must_have_flags(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@student.uj.edu.pl", password=PASSWORD, is_superuser=False
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@student.uj.edu.pl", password=PASSWORD, is_staff=False
            )


class PasswordHashingTests(TestCase):
    def test_password_is_hashed_with_argon2(self):
        user = User.objects.create_user(email="jan@student.uj.edu.pl", password=PASSWORD)
        self.assertTrue(user.password.startswith("argon2$"))
        self.assertNotIn(PASSWORD, user.password)
        self.assertTrue(user.check_password(PASSWORD))
        self.assertFalse(user.check_password("zle-haslo"))


class EmailLoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="jan@student.uj.edu.pl", password=PASSWORD, is_active=True
        )

    def test_authenticate_with_email(self):
        self.assertEqual(authenticate(email="jan@student.uj.edu.pl", password=PASSWORD), self.user)

    def test_authenticate_is_case_insensitive(self):
        self.assertEqual(authenticate(email="JAN@Student.UJ.edu.pl", password=PASSWORD), self.user)

    def test_wrong_password_is_rejected(self):
        self.assertIsNone(authenticate(email="jan@student.uj.edu.pl", password="zle-haslo"))

    def test_inactive_user_cannot_log_in(self):
        self.user.is_active = False
        self.user.save()
        self.assertIsNone(authenticate(email="jan@student.uj.edu.pl", password=PASSWORD))

    def test_client_login_with_email(self):
        self.assertTrue(self.client.login(email="jan@student.uj.edu.pl", password=PASSWORD))


class UserAdminTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email="admin@student.uj.edu.pl", password=PASSWORD)
        self.client.force_login(self.admin)

    def test_changelist_page(self):
        response = self.client.get(reverse("admin:accounts_user_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_add_page(self):
        response = self.client.get(reverse("admin:accounts_user_add"))
        self.assertEqual(response.status_code, 200)

    def test_change_page(self):
        response = self.client.get(reverse("admin:accounts_user_change", args=[self.admin.pk]))
        self.assertEqual(response.status_code, 200)
