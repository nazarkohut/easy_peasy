from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
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

    def validate(self, attrs): # Same as below
        request = self.context['request']
        if request.parser_context['kwargs']:
            raise NotFound(detail="Not Found", code=404)
        return attrs


class UpdateProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(required=True, allow_blank=False)  # Have to make this one required

    class Meta:
        model = UserProfile
        fields = ['image']

    def validate(self, attrs): # Same as above, some improvements may be applied
        request = self.context['request']
        if request.parser_context['kwargs']:
            raise NotFound(detail="Not Found", code=404)
        return attrs


# ------------------------------------------------------------------------
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['password', 'password2', 'old_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.get_user(self.context['request'])
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.get_user(self.context['request'])
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You don't have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    @staticmethod
    def get_user(data):
        return data.user
