from django.utils.encoding import force_text

from ..test_setup import TestSetup


class TestResetPassword(TestSetup):
    def test_empty_reset_password(self):
        data = {}
        response = self.client.post(path=self.reset_password_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"email": ["This field is required."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_blank_email_reset_password(self):
        data = {"email": ""}
        response = self.client.post(path=self.reset_password_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"email":["This field may not be blank."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_invalid_email_reset_password(self):
        data = {"email": "invalid_email_address@g"}
        response = self.client.post(path=self.reset_password_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"email": ["Enter a valid email address."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_email_not_found_reset_password(self):
        data = {"email": "email_that_does_not_exist@gmail.com"}
        response = self.client.post(path=self.reset_password_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"non_field_errors": ["User with given email does not exist."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_success_reset_password(self):
        data = {"email": "tutahore@norwegischlernen.info"}
        response = self.client.post(path=self.reset_password_url, data=data)
        self.assertEqual(response.status_code, 204)

