from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'image']


class UpdateProfileSerializer(serializers.ModelSerializer):
    userprofile = ProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'userprofile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', None)
        if profile_data is not None:

            user = self.context['request'].user

            if user.pk != instance.pk:
                raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

            instance.userprofile.bio = profile_data['bio']
            instance.userprofile.location = profile_data['location']
            instance.userprofile.save()
        return super().update(instance, validated_data)


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
        user = self.context['request'].user  # same
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user  # same
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
