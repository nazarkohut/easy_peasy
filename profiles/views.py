# from rest_framework.authtoken.admin import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from profiles.serializers import ProfileSerializer, UpdateProfileSerializer


class ProfileView(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        profile_serializer = ProfileSerializer(user.userprofile)
        return Response(profile_serializer.data)


class EditProfileView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    queryset = get_user_model().objects.all()

