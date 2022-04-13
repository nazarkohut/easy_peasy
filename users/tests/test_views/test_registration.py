from django.utils.encoding import force_text
from rest_framework.reverse import reverse

from users.tests.test_setup import TestSetup


class TestRegistration(TestSetup):

    def test_empty_registration(self):
        data = {}
        response = self.client.post(reverse("user-list"), data=data, format='json')
        error = {'email': ['This field is required.'], 'first_name': ['This field is required.'],
                 'last_name': ['This field is required.'], 'username': ['This field is required.'],
                 'password': ['This field is required.']}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_wrong_email1_registration(self):
        data = {
            "email": "tutahore@norwegischlerneninfo",
            "first_name": "first_name",
            "last_name": "last_name",
            "username": "username1",
            "password": "password"
        }
        response = self.client.post(reverse("user-list"), data=data, format='json')
        error = {"non_field_errors": ["Enter a valid email address."]}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_wrong_email2_registration(self):
        data = {
            "email": "tutahorenorwegischlernen.info",
            "first_name": "first_name",
            "last_name": "last_name",
            "username": "username1",
            "password": "password"
        }
        response = self.client.post(reverse("user-list"), data=data, format='json')
        error = {"non_field_errors": ["Email should contain '@' sign"]}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_wrong_email3_registration(self):
        data = {
            "email": "tutahore@norwegischlernen.i",
            "first_name": "first_name",
            "last_name": "last_name",
            "username": "username1",
            "password": "password"
        }
        response = self.client.post(reverse("user-list"), data=data, format='json')
        error = {'non_field_errors': ['Enter a valid email address.']}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_unique_username_registration(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "first_name": "first_name",
            "last_name": "last_name",
            "username": "username",
            "password": "password"
        }
        response = self.client.post(reverse("user-list"), data=data, format='json')
        error = {"username": ["A user with that username already exists."]}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_unique_email_registration(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "first_name": "first_name",
            "last_name": "last_name",
            "username": "username1",
            "password": "password"
        }
        response = self.client.post(reverse("user-list"), data=data, format='json')
        error = {"non_field_errors": ["User with this email already exist"]}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_password_length_registration(self):
        data = {"email": "email1@gmail.com",
                "first_name": "first_name",
                "last_name": "last_name",
                "username": "username1",
                "password": "passw"}
        response = self.client.post(reverse("user-list"), data=data, format='json')
        expected_response = {"password": ["Ensure this field has at least 6 characters."]}
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response_content, expected_response)

    def test_successful_registration(self):
        data = {"email": "email1@gmail.com",
                "first_name": "first_name",
                "last_name": "last_name",
                "username": "username1",
                "password": "password"}
        response = self.client.post(reverse("user-list"), data=data, format='json')
        expected_response = {"email": "email1@gmail.com",
                             "first_name": "first_name",
                             "last_name": "last_name",
                             "username": "username1"}
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(response_content, expected_response)
