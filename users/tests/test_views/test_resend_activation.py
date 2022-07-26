from django.utils.encoding import force_text

from users.tests.test_auth_setup import TestAuthenticationSetup


class TestResendActivation(TestAuthenticationSetup):
    def test_empty_body(self):
        data = {}
        response = self.client.post(path=self.resend_activation_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"email": ["This field is required."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_blank_fields(self):
        data = {"email": ""}
        response = self.client.post(path=self.resend_activation_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"email": ["This field may not be blank."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_invalid_email(self):
        data = {"email": "invalid_email"}
        response = self.client.post(path=self.resend_activation_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"email": ["Enter a valid email address."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_max_length_email(self):
        data = {"email": "some_really_long_email" * self.big_number + "@gmail.com"}
        response = self.client.post(path=self.resend_activation_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"email": [f"Ensure this field has no more than {self.email_max_length} characters."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_email_not_found(self):
        data = {"email": "email_that_does_not_exist@gmail.com"}
        response = self.client.post(path=self.resend_activation_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"non_field_errors": ["User with given email does not exist."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_user_already_activated(self):
        data = {"email": self.user.email}
        response = self.client.post(path=self.resend_activation_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"non_field_errors": ["User with this email already activated."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_success(self):
        data = {"email": self.not_active_user.email}
        response = self.client.post(path=self.resend_activation_url, data=data, format='json')
        self.assertEqual(response.status_code, 204)
