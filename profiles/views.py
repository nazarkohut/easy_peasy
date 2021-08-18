from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from profiles.serializers import ProfileSerializer, UpdateProfileSerializer, ChangePasswordSerializer


class ProfileView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        profile_serializer = ProfileSerializer(user.userprofile)
        return Response(profile_serializer.data)


class EditProfileView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UpdateProfileSerializer
    queryset = get_user_model().objects.all()


class ChangePassword(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
