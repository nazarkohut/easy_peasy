from django.utils.encoding import force_text

from users.tests.test_setup import TestSetup


class TestLogin(TestSetup):
    def test_empty_login(self):
        data = {}
        response = self.client.post(self.login_url, data=data)
        error = {"username": ["This field is required."], "password": ["This field is required."]}
        self.assertJSONEqual(force_text(response.content), error)
        self.assertEqual(response.status_code, 400)

    def test_blank_email_login(self):
        data = {
            "email": "",
            "password": "password"
        }
        response = self.client.post(self.login_url, data=data)
        error = {'email': ['This field may not be blank.']}
        self.assertJSONEqual(force_text(response.content), error)
        self.assertEqual(response.status_code, 400)

    def test_blank_username_login(self):
        data = {
            "username": "",
            "password": "password"
        }
        response = self.client.post(self.login_url, data=data)
        error = {'username': ['This field may not be blank.']}
        self.assertJSONEqual(force_text(response.content), error)
        self.assertEqual(response.status_code, 400)

    def test_email_does_not_exist(self):
        data = {
            "email": "tutahore@norwegischlernen.inf",
            "password": "password"
        }
        response = self.client.post(self.login_url, data=data)
        error = {"non_field_errors": ["User with given email does not exist."]}
        self.assertJSONEqual(force_text(response.content), error)
        self.assertEqual(response.status_code, 400)

    def test_username_does_not_exist(self):
        data = {
            "username": "username1000",
            "password": "password"
        }
        response = self.client.post(self.login_url, data=data)
        error = {"non_field_errors": ["User with given username does not exist."]}
        self.assertJSONEqual(force_text(response.content), error)
        self.assertEqual(response.status_code, 400)

    # fields errors
    def test_username_length(self):
        data = {
            "username": "Username" * 100,
            "password": "password"
        }
        response = self.client.post(self.login_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"username": ["Ensure this field has no more than 128 characters."]}
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_username_isalnum(self):
        data = {
            "username": "User_name",
            "password": "password"
        }
        response = self.client.post(self.login_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"username": ["This field should contain only alphanumeric character"]}
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_email_length(self):
        data = {
            "email": "email" * 100 + "@gmail.com",
            "password": "password"
        }
        response = self.client.post(self.login_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"email": ["Ensure this field has no more than 254 characters."]}
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    # password length
    def test_password_length_email_login(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "password": "passw"
        }
        response = self.client.post(self.login_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"password": ["Ensure this field has at least 6 characters."]}
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    def test_password_length_username_login(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "password": "passw"
        }
        response = self.client.post(self.login_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"password": ["Ensure this field has at least 6 characters."]}
        response_content = force_text(response.content)
        self.assertJSONEqual(response_content, error)

    # Wrong credentials
    def test_wrong_credentials_email_login(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "password": "wrong_password"
        }
        response = self.client.post(self.login_url, data=data)
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 400)
        error = {"detail": ["This credentials did not work. Please, try again."]}
        self.assertJSONEqual(response_content, error)

    def test_wrong_credentials_username_login(self):
        data = {
            "username": "username",
            "password": "wrong_password"
        }
        response = self.client.post(self.login_url, data=data)
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 400)
        error = {"detail": ["This credentials did not work. Please, try again."]}
        self.assertJSONEqual(response_content, error)

    # User is not active
    def test_user_is_not_active_username_login(self):
        data = {
            "username": "notActiveUsername",
            "password": "password"
        }
        response = self.client.post(self.login_url, data=data)
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 400)
        error = {"detail": ["No active account found with the given credentials. "
                            "Note: please, make sure you activated your account."]}
        self.assertJSONEqual(response_content, error)

    def test_user_is_not_active_email_login(self):
        data = {
            "email": "not_active_user@gmail.com",
            "password": "password"
        }
        response = self.client.post(self.login_url, data=data)
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 400)
        error = {"detail": ["No active account found with the given credentials. "
                            "Note: please, make sure you activated your account."]}
        self.assertJSONEqual(response_content, error)

    # Successful
    def test_successful_email_login(self):
        data = {
            "email": "tutahore@norwegischlernen.info",
            "password": "password"
        }
        response = self.client.post(self.login_url, data=data)
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIn("refresh", container=response_content)
        self.assertIn("access", container=response_content)

    def test_successful_username_login(self):
        data = {
            "username": "username",
            "password": "password"
        }
        response = self.client.post(self.login_url, data=data)
        response_content = force_text(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIn("refresh", container=response_content)
        self.assertIn("access", container=response_content)
