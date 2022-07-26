from django.utils.encoding import force_text

from profiles.tests.test_auth_setup import TestProfileAuthenticationSetup


class TestEditProfile(TestProfileAuthenticationSetup):
    first_name_max_length = 64
    last_name_max_length = 64
    bio_max_length = 256
    location_max_length = 128

    def test_unauthorized_access_to_edit_profile(self):
        response = self.client.put(path=self.edit_url)
        error = {"detail": "Authentication credentials were not provided."}
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(force_text(response.content), error)

    def test_empty_body(self):
        super().authenticate(user='current')
        empty_body = {}
        response = self.client.put(self.edit_url, data=empty_body, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"first_name": ["This field is required."], "last_name": ["This field is required."],
                 "user_profile": ["This field is required."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_blank_fields(self):
        data = {"first_name": "", "last_name": "", "user_profile": {
            "bio": "",
            "location": ""
        }}
        super().authenticate(user='current')
        response = self.client.put(self.edit_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"first_name": ["This field may not be blank."], "last_name": ["This field may not be blank."]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_isalnum_fields(self):
        data = {"first_name": "first_name", "last_name": "last_name", "user_profile": {}}
        super().authenticate(user='current')
        response = self.client.put(self.edit_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"first_name": ["This field should contain only alphanumeric character"],
                 "last_name": ["This field should contain only alphanumeric character"]}
        self.assertJSONEqual(force_text(response.content), error)

    def test_max_length_of_fields(self):
        super().authenticate(user='current')
        data = {"first_name": "firstname" * self.big_number, "last_name": "lastname" * self.big_number,
                "user_profile": {
                    "bio": "some_bio" * self.big_number, "location": "location" * self.big_number
                }}
        response = self.client.put(path=self.edit_url, data=data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"first_name": [f"Ensure this field has no more than {self.first_name_max_length} characters."],
                 "last_name": [f"Ensure this field has no more than {self.last_name_max_length} characters."],
                 "user_profile": {
                     "bio":
                         [f"Ensure this field has no more than {self.bio_max_length} characters."],
                     "location":
                         [f"Ensure this field has no more than {self.location_max_length} characters."]
                 }}
        self.assertJSONEqual(force_text(response.content), error)

    def test_wrong_data_types(self):
        super().authenticate(user='current')
        data = {"first_name": [], "last_name": {}, "user_profile": []}
        response = self.client.put(self.edit_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        error = {"first_name": ["Not a valid string."], "last_name": ["Not a valid string."], "user_profile":
            {'non_field_errors': ['Invalid data. Expected a dictionary, but got list.']}}
        self.assertJSONEqual(force_text(response.content), error)

    def test_successful_profile_edit(self):
        super().authenticate(user='current')
        data = {"first_name": "newFirstName",
                "last_name": "newLastName",
                "user_profile": {
                    "bio": "newBio",
                    "location":
                        "newLocation"
                }}
        response = self.client.put(path=self.edit_url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_text(response.content), data)

    def test_successful_profile_edit_with_additional_parameters(self):
        super().authenticate(user='current')
        data = {"first_name": "newFirstName",
                "last_name": "newLastName",
                "user_profile": {
                    "bio": "newBio",
                    "location":
                        "newLocation",
                    "additional_parameter": "additional parameter data"
                },
                "additional_parameter": "additional parameter data"
                }
        response = self.client.put(path=self.edit_url, data=data, format='json')
        self.assertEqual(response.status_code, 200)
        expected_data = {"first_name": "newFirstName",
                         "last_name": "newLastName",
                         "user_profile": {
                             "bio": "newBio",
                             "location":
                                 "newLocation"
                         }}
        self.assertJSONEqual(force_text(response.content), expected_data)
