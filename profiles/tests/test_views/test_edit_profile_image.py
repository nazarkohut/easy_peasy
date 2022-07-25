from django.utils.encoding import force_text

from profiles.tests.test_auth_setup import TestProfileAuthenticationSetup


class TestEditProfile(TestProfileAuthenticationSetup):
    def test_unauthorized_access_to_edit_profile_image(self):
        response = self.client.patch(path=self.edit_url)
        error = {"detail": "Authentication credentials were not provided."}
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(force_text(response.content), error)

    def test_empty_body(self):
        super().authenticate(user='current')
        data = {}
        response = self.client.patch(path=self.edit_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"image": ["This field is required."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_blank_fields(self):
        super().authenticate(user='current')
        data = {"image": ""}
        response = self.client.patch(path=self.edit_url, data=data)
        self.assertEqual(response.status_code, 400)
        error = {"image": ["This field may not be blank."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_wrong_data_type(self):
        super().authenticate(user='current')
        data = {"image": []}
        response = self.client.patch(path=self.edit_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"image": ["Not a valid string."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_success(self):
        super().authenticate(user='current')
        data = {"image": "https://cloudinary.com/image_url"}
        response = self.client.patch(path=self.edit_url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        response_data = {"image": "https://cloudinary.com/image_url"}
        self.assertJSONEqual(force_text(response.content), response_data)
