from django.utils.encoding import force_text
from djoser import urls
from rest_framework.reverse import reverse

from users.tests.test_auth_setup import TestAuthenticationSetup


class TestLogout(TestAuthenticationSetup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_unauthenticated_logout(self):
        data = {"refresh": self.curr_user['refresh']}
        response = self.client.post(path=self.logout_url, data=data)
        self.assertEqual(response.status_code, 401)
        error = {"detail": "Authentication credentials were not provided."}
        self.assertJSONEqual(force_text(response.content), error)

    def test_empty_logout(self):
        super().authenticate(user='current')
        data = {}
        response = self.client.post(path=self.logout_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"refresh": ["This field is required"]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_invalid_token_logout(self):
        super().authenticate(user='current')
        data = {"refresh": "invalid_refresh_token"}
        response = self.client.post(path=self.logout_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"message": "Token is invalid or expired"}
        self.assertJSONEqual(force_text(response.content), error)

    def test_blank_token_logout(self):
        super().authenticate(user='current')
        data = {"refresh": ""}
        response = self.client.post(path=self.logout_url, data=data)
        self.assertEqual(response.status_code, 400)
        expected_response = {"refresh": ["May not be blank"]}
        self.assertJSONEqual(force_text(response.content), expected_response)

    def test_another_user_logout(self):
        super().authenticate(user='another')
        data = {"refresh": self.curr_user['refresh']}
        response = self.client.post(path=self.logout_url, data=data)
        self.assertEqual(response.status_code, 403)
        expected_response = {"detail": "You do not have permission to logout another user"}
        self.assertJSONEqual(force_text(response.content), expected_response)

    def test_successful_logout(self):
        refresh, access = super().authenticate(user='current')
        data = {"refresh": refresh}
        response = self.client.post(path=self.logout_url, data=data)
        self.assertEqual(response.status_code, 200)
        expected_response = {'message': 'Success'}
        self.assertJSONEqual(force_text(response.content), expected_response)
        # expired token subtest
        self.expired_token_logout()

    def expired_token_logout(self):
        refresh, access = super().authenticate(user='current')
        data = {"refresh": refresh}
        response = self.client.post(path=self.logout_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"message": "Token is invalid or expired"}
        self.assertJSONEqual(force_text(response.content), error)
