from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['bio', 'location']


class UpdateProfileSerializer(serializers.ModelSerializer):
    userprofile = ProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'userprofile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', None)
        if profile_data is not None:
            instance.userprofile.bio = profile_data['bio']
            instance.userprofile.location = profile_data['location']
            instance.userprofile.save()
        return super().update(instance, validated_data)
