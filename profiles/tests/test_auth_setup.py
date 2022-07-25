from rest_framework.reverse import reverse

from users.tests.test_auth_setup import TestAuthenticationSetup


class TestProfileAuthenticationSetup(TestAuthenticationSetup):
    edit_url = reverse('edit')
