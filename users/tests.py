from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegisterViewTest(TestCase):
    def test_get_200(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_valid_registration_creates_user(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "TestPass#123",
            "password2": "TestPass#123",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_valid_registration_redirects_to_login(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser2",
            "email": "new2@example.com",
            "password1": "TestPass#123",
            "password2": "TestPass#123",
        })
        self.assertRedirects(response, reverse("login"))

    def test_invalid_registration_shows_form(self):
        response = self.client.post(reverse("register"), {
            "username": "u",
            "password1": "pass",
            "password2": "different",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="u").exists())

    def test_profile_created_on_registration(self):
        self.client.post(reverse("register"), {
            "username": "profileuser",
            "email": "p@example.com",
            "password1": "TestPass#123",
            "password2": "TestPass#123",
        })
        user = User.objects.get(username="profileuser")
        self.assertTrue(hasattr(user, "profile"))


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("testuser", "t@t.com", "TestPass#123")

    def test_get_200(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "TestPass#123",
        })
        self.assertEqual(response.status_code, 302)

    def test_login_failure_stays_on_page(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "wrongpass",
        })
        self.assertEqual(response.status_code, 200)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("profuser", "p@p.com", "TestPass#123")

    def test_profile_redirects_anonymous(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response["Location"])

    def test_profile_get_authenticated(self):
        self.client.login(username="profuser", password="TestPass#123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_profile_update_username(self):
        self.client.login(username="profuser", password="TestPass#123")
        response = self.client.post(reverse("profile"), {
            "username": "profuser_updated",
            "email": "updated@p.com",
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "profuser_updated")
