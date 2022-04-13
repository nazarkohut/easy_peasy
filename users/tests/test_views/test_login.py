from django.utils.encoding import force_text
from rest_framework.reverse import reverse

from users.tests.test_setup import TestSetup


class TestLogin(TestSetup):
    def test_empty_login(self):
        data = {}
        response = self.client.post(reverse("login"), data=data)
        error = {"username": ["This field is required."], "password": ["This field is required."]}
        self.assertJSONEqual(force_text(response.content), error)
        self.assertEqual(response.status_code, 400)

    def test_blank_email_login(self):
        data = {
            "email": "",
            "password": "password"
        }
        response = self.client.post(reverse("login"), data=data)
        error = {'email': ['This field may not be blank.']}
        self.assertJSONEqual(force_text(response.content), error)
        self.assertEqual(response.status_code, 400)

    def test_blank_username_login(self):
        data = {
            "username": "",
            "password": "password"
        }
        response = self.client.post(reverse("login"), data=data)
        error = {'username': ['This field may not be blank.']}
        self.assertJSONEqual(force_text(response.content), error)
        self.assertEqual(response.status_code, 400)

    def test_email_does_not_exist(self):
        data = {
            "email": "tutahore@norwegischlernen.inf",
            "password": "password"
        }
        response = self.client.post(reverse("login"), data=data)
        error = {"non_field_errors": ["User with given email does not exist."]}
        self.assertJSONEqual(force_text(response.content), error)
        self.assertEqual(response.status_code, 400)

    def test_username_does_not_exist(self):
        data = {
            "username": "username1000",
            "password": "password"
        }
        response = self.client.post(reverse("login"), data=data)
        error = {"non_field_errors": ["User with given username does not exist."]}
        self.assertJSONEqual(force_text(response.content), error)
        self.assertEqual(response.status_code, 400)

    def test_email_password_length(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "password": "passw"
        }
        response = self.client.post(reverse("login"), data=data)
        self.assertEqual(response.status_code, 400)
        error = {"password": ["Ensure this field has at least 6 characters."]}
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_username_password_length(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "password": "passw"
        }

        response = self.client.post(reverse("login"), data=data)
        self.assertEqual(response.status_code, 400)
        error = {"password": ["Ensure this field has at least 6 characters."]}
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_successful_email_login(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "password": "password"
        }
        response = self.client.post(reverse("login"), data=data)
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIn("refresh", container=response_content)
        self.assertIn("access", container=response_content)

    def test_successful_username_login(self):
        data = {
            "username": "username",
            "password": "password"
        }
        response = self.client.post(reverse("login"), data=data)
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIn("refresh", container=response_content)
        self.assertIn("access", container=response_content)
