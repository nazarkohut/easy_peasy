from django.utils.encoding import force_text
from rest_framework.reverse import reverse

from profiles.tests.test_auth_setup import TestProfileAuthenticationSetup


class TestProfile(TestProfileAuthenticationSetup):
    def test_unauthorized_access_to_profile(self):
        profile_that_does_not_exist = reverse('profile', [1])
        response = self.client.get(path=profile_that_does_not_exist)
        error = {"detail": "Authentication credentials were not provided."}
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(force_text(response.content), error)

    def test_profile_not_found(self):
        super().authenticate(user='current')
        profile_that_does_not_exist_url = reverse('profile', [100_000_000])
        response = self.client.get(path=profile_that_does_not_exist_url)
        self.assertEqual(response.status_code, 404)
        error = {"detail": "Not found."}
        self.assertJSONEqual(force_text(response.content), error)

    def test_profile_of_not_active_user(self):
        super().authenticate(user='current')
        not_active_user_id = self.not_active_user.id
        not_active_user_url = reverse('profile', [not_active_user_id])
        response = self.client.get(path=not_active_user_url)
        self.assertEqual(response.status_code, 404)
        error = {"detail": "Not Found"}
        self.assertJSONEqual(force_text(response.content), error)

    def test_profile_that_user_owns(self):
        super().authenticate(user='current')
        active_user_id = self.user.id
        active_user_url = reverse('profile', [active_user_id])
        response = self.client.get(path=active_user_url)
        self.assertEqual(response.status_code, 200)

    def test_profile_that_user_does_not_own(self):
        super().authenticate(user='another')
        active_user_id = self.user.id
        active_user_url = reverse('profile', [active_user_id])
        response = self.client.get(path=active_user_url)
        self.assertEqual(response.status_code, 200)
