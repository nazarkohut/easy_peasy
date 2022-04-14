from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class TestSetup(APITestCase):
    def setUp(self):
        # users
        self.user = User.objects.create_user(
            email="tutahore@norwegischlernen.info",
            first_name="first_name",
            last_name="last_name",
            username="username",
            password="password")

        self.another_user = User.objects.create_user(
            email="another_tutahore@norwegischlernen.info",
            first_name="first_name",
            last_name="last_name",
            username="another_username",
            password="password")

        # urls
        self.login_url = reverse('login')
        self.registration_url = reverse("user-list")
        self.reset_password_url = reverse('user-reset-password')
        self.logout_url = reverse('logout')
