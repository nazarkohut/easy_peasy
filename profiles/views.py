from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from profiles.models import UserProfile
from profiles.serializers import ProfileSerializer, UpdateProfileSerializer, ChangePasswordSerializer, \
    UpdateProfileImageSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        if not user.is_active:
            raise NotFound(detail="Not Found", code=404)
        profile_serializer = ProfileSerializer(user.user_profile)
        return Response(profile_serializer.data)

    def get_object(self, **kwargs):
        user_id = self.request.user.id
        if 'type' in kwargs and kwargs['type'] == 'patch':
            return get_object_or_404(UserProfile, user_id=user_id)
        return get_object_or_404(self.get_queryset(), pk=user_id)

    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateProfileSerializer
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.serializer_class = UpdateProfileImageSerializer
        self.get_serializer(self.get_object(type='patch'))
        return super().patch(request, *args, **kwargs)


class ChangePassword(generics.UpdateAPIView):  # Perhaps, will be changed to djoser change password
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
