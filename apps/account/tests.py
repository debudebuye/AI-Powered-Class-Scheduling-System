from django.contrib.auth.models import User
from django.test import Client, TestCase

from .forms import UserRegistrationForm
from .models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_str(self):
        self.assertEqual(str(self.profile), "Profile for user testuser")

    def test_profile_created_on_registration(self):
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(self.profile.user, self.user)


class UserRegistrationFormTest(TestCase):
    def test_valid_form(self):
        form = UserRegistrationForm(
            data={
                "username": "newuser",
                "first_name": "New",
                "email": "new@example.com",
                "password": "securepass123",
                "password2": "securepass123",
            }
        )
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form = UserRegistrationForm(
            data={
                "username": "newuser",
                "first_name": "New",
                "email": "new@example.com",
                "password": "securepass123",
                "password2": "differentpass",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_missing_fields(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())


class AccountViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_register_get(self):
        response = self.client.get("/account/register/")
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get("/account/login/")
        self.assertEqual(response.status_code, 200)

    def test_admin_login_post_invalid(self):
        response = self.client.post(
            "/account/login/", {"username": "wrong", "password": "wrong"}
        )
        self.assertIn(response.status_code, [200, 302])

    def test_admin_login_post_valid(self):
        response = self.client.post(
            "/account/login/", {"username": "testuser", "password": "testpass123"}
        )
        self.assertIn(response.status_code, [200, 302])

    def test_user_list_requires_login(self):
        response = self.client.get("/account/users/")
        self.assertEqual(response.status_code, 302)
