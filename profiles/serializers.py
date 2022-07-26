from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from misc.validators import isalnum_validator
from profiles.models import UserProfile
from tests.models import TestResult


class TestsForProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ['id', 'mark', 'test_time']


class ProfileSerializer(serializers.ModelSerializer):
    previous_tests = TestsForProfileSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'image', 'previous_tests']


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(source='user_profile')

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "last_login", "date_joined", "profile")
        # may be included in future as well "groups": [], "user_permissions": []


# --------------------------------------------
class ProfileForUpdateSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(max_length=256, required=False, allow_blank=True)
    location = serializers.CharField(max_length=128, required=False, allow_blank=True)

    class Meta:
        model = UserProfile
        fields = ['bio', 'location']


class UpdateProfileSerializer(serializers.ModelSerializer):
    user_profile = ProfileForUpdateSerializer()
    first_name = serializers.CharField(required=True, max_length=64, validators=[isalnum_validator])
    last_name = serializers.CharField(required=True, max_length=64, validators=[isalnum_validator])

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'user_profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('user_profile', None)
        if profile_data is not None:
            instance.user_profile.bio = profile_data.get('bio', '')
            instance.user_profile.location = profile_data.get('location', '')
            instance.user_profile.save()
        return super().update(instance, validated_data)

    def validate(self, attrs):
        request = self.context['request']
        if request.parser_context['kwargs']:
            raise NotFound(detail="Not Found", code=404)
        return attrs


class UpdateProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(required=True, allow_blank=False)

    # required attribute does not work here(so do not try to simplify validate method)

    class Meta:
        model = UserProfile
        fields = ['image']

    def validate(self, attrs):
        if 'image' not in attrs:
            raise serializers.ValidationError({"image": ["This field is required."]})
        request = self.context['request']
        if request.parser_context['kwargs']:
            raise NotFound(detail="Not Found", code=404)
        return attrs
