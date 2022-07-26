from django.utils.encoding import force_text

from users.tests.test_setup import TestSetup


class TestRegistration(TestSetup):
    def test_empty_registration(self):
        data = {}
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {'email': ['This field is required.'], 'first_name': ['This field is required.'],
                 'last_name': ['This field is required.'], 'username': ['This field is required.'],
                 'password': ['This field is required.']}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_wrong_email1_registration(self):
        data = {
            "email": "tutahore@norwegischlerneninfo",
            "first_name": "first",
            "last_name": "last",
            "username": "username1",
            "password": "password"
        }
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {"non_field_errors": ["Enter a valid email address."]}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_wrong_email2_registration(self):
        data = {
            "email": "tutahorenorwegischlernen.info",
            "first_name": "first",
            "last_name": "last",
            "username": "username1",
            "password": "password"
        }
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {"email": ["Email should contain '@' sign"]}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_wrong_email3_registration(self):
        data = {
            "email": "tutahore@norwegischlernen.i",
            "first_name": "first",
            "last_name": "last",
            "username": "username1",
            "password": "password"
        }
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {'non_field_errors': ['Enter a valid email address.']}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    # unique errors
    def test_unique_username_registration(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "first_name": "First",
            "last_name": "Last",
            "username": "username",
            "password": "password"
        }
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {'non_field_errors': ['User with this email already exist']}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_unique_email_registration(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "first_name": "first",
            "last_name": "last",
            "username": "username1",
            "password": "password"
        }
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {'non_field_errors': ['User with this email already exist']}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    # fields length
    def test_max_email_length_registration(self):
        data = {
            # note that email will be checked after all fields(that is why we do not have unique email error in here)
            "email": "tutahore" * 32 + "@norwegischlernen.info",
            "first_name": "first",
            "last_name": "last",
            "username": "username1",
            "password": "password"
        }
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {"email": [f"Ensure this field has no more than {self.email_max_length} characters."]}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_max_username_length_registration(self):
        data = {
            # note that email will be checked after all fields(that is why we do not have unique email error in here)
            "email": "tutahore@norwegischlernen.info",
            "first_name": "first",
            "last_name": "last",
            "username": "username" * 25,
            "password": "password"
        }
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {"username": [f"Ensure this field has no more than {self.username_max_length} characters."]}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_max_first_name_length_registration(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "first_name": "first" * 14,
            "last_name": "last",
            "username": "username1",
            "password": "password"
        }
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {"first_name": ["Ensure this field has no more than 64 characters."]}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_max_last_name_length_registration(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "first_name": "first",
            "last_name": "last" * 20,
            "username": "username1",
            "password": "password"
        }
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {"last_name": ["Ensure this field has no more than 64 characters."]}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_max_password_length_registration(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "first_name": "first",
            "last_name": "last",
            "username": "username1",
            "password": "password" * 9
        }
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {"password": ["Ensure this field has no more than 64 characters."]}
        self.assertEqual(response.status_code, 400)
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_min_password_length_registration(self):
        data = {"email": "email1@gmail.com",
                "first_name": "first",
                "last_name": "last",
                "username": "username1",
                "password": "passw"}
        response = self.client.post(self.registration_url, data=data, format='json')
        expected_response = {"password": [f"Ensure this field has at least {self.password_min_length} characters."]}
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response_content, expected_response)

    # Alpha numeric fields
    def test_username_isalnum_registration(self):
        data = {"email": "email1@gmail.com",
                "first_name": "first",
                "last_name": "last",
                "username": "user name",
                "password": "password"}
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {"username": ["This field should contain only alphanumeric character"]}
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response_content, error)

    def test_last_name_isalnum_registration(self):
        data = {"email": "email1@gmail.com",
                "first_name": "first",
                "last_name": "last_name",
                "username": "username",
                "password": "password"}
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {"last_name": ["This field should contain only alphanumeric character"]}
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response_content, error)

    def test_isalnum_last_and_first_name_registration(self):
        data = {"email": "email2@gmail.com",
                "first_name": "first_name",
                "last_name": "last_name",
                "username": "username",
                "password": "password"}
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {"first_name": ["This field should contain only alphanumeric character"],
                 "last_name": ["This field should contain only alphanumeric character"]}
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response_content, error)

    def test_isalnum_fields_registration(self):
        data = {"email": "email1@gmail.com",
                "first_name": "first_name",
                "last_name": "last_name",
                "username": "username_",
                "password": "password"}
        response = self.client.post(self.registration_url, data=data, format='json')
        error = {"first_name": ["This field should contain only alphanumeric character"],
                 "last_name": ["This field should contain only alphanumeric character"],
                 "username": ["This field should contain only alphanumeric character"]}
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response_content, error)

    # Successful
    def test_successful_registration(self):
        data = {"email": "email1@gmail.com",
                "first_name": "first",
                "last_name": "last",
                "username": "username1",
                "password": "password"}
        response = self.client.post(self.registration_url, data=data, format='json')
        expected_response = {"email": "email1@gmail.com",
                             "first_name": "first",
                             "last_name": "last",
                             "username": "username1"}
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(response_content, expected_response)
