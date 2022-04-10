from django.contrib.auth.models import User
from django.utils.encoding import force_text
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestRegistration(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="tutahore@norwegischlernen.info",
            first_name="first_name",
            last_name="last_name",
            username="username",
            password="password")

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


class TestLogin(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="tutahore@norwegischlernen.info",
            first_name="first_name",
            last_name="last_name",
            username="username",
            password="password")

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


# print(urls.base.urlpatterns)
