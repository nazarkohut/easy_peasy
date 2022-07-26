from django.utils.encoding import force_text

from users.tests.test_auth_setup import TestAuthenticationSetup


class TestSetPassword(TestAuthenticationSetup):
    def test_unauthorized(self):
        data = {}
        response = self.client.post(path=self.set_password_url, data=data, format='json')
        self.assertEqual(response.status_code, 401)
        error = {"detail": "Authentication credentials were not provided."}
        self.assertJSONEqual(force_text(response.content), error)

    def test_empty_body(self):
        super().authenticate(user='current')
        data = {}
        response = self.client.post(path=self.set_password_url, data=data, format='json')
        error = {"new_password": ["This field is required."], "current_password": ["This field is required."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_blank_fields(self):
        super().authenticate(user='current')
        data = {"current_password": "", "new_password": ""}
        response = self.client.post(path=self.set_password_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"current_password": ["This field may not be blank."], "new_password": ["This field may not be blank."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_min_length(self):
        super().authenticate(user='current')
        user_password = "password"
        data = {"current_password": user_password, "new_password": "c"}
        response = self.client.post(path=self.set_password_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"new_password": ["Ensure this field has at least 8 characters."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_max_length(self):
        super().authenticate(user='current')
        data = {"current_password": "c" * self.big_number, "new_password": "c" * self.big_number}
        response = self.client.post(path=self.set_password_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"new_password": [f"Ensure this field has no more than {self.password_max_length} characters."],
                 "current_password": [f"Ensure this field has no more than {self.password_max_length} characters."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_wrong_current_password(self):
        super().authenticate(user='current')
        data = {"current_password": "some_not_valid_password", "new_password": "some_new_password"}
        response = self.client.post(path=self.set_password_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"current_password": ["Invalid password."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_common_password(self):
        super().authenticate(user='current')
        user_password = "password"
        data = {"current_password": user_password, "new_password": "password"}
        response = self.client.post(path=self.set_password_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"new_password": ["This password is too common."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_success(self):
        super().authenticate(user='current')
        user_password = "password"
        data = {"current_password": user_password, "new_password": "SomeStr()ngPass0rD"}
        response = self.client.post(path=self.set_password_url, data=data, format='json')
        self.assertEqual(response.status_code, 204)
