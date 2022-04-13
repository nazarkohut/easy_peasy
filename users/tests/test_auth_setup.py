from rest_framework.reverse import reverse

from users.tests.test_setup import TestSetup


class TestAuthenticationSetup(TestSetup):
    def setUp(self):
        super().setUp()
        self.curr_user = self.client.post(
            path=reverse('login'),
            data={"username": "username",
                  "password": "password"}, format='json').data

        self.another_user = self.client.post(
            path=reverse('login'),
            data={"username": "another_username",
                  "password": "password"}, format='json').data

    def authenticate(self, user: str):
        if user == 'current':
            refresh, access = self.curr_user['refresh'], self.curr_user['access']
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
            return refresh, access
        refresh, access = self.another_user['refresh'], self.another_user['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        return refresh, access