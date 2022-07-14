from djoser.views import UserViewSet
from rest_framework import status, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from easy_peasy import settings
from users.serializers import EmailTokenObtainPairSerializer, UsernameTokenObtainPairSerializer, BlackListSerializer, \
    CustomResendActivationEmailSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    def get_serializer_class(self):
        if "email" in self.request.data:
            return EmailTokenObtainPairSerializer
        return UsernameTokenObtainPairSerializer


class BlacklistRefreshView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = BlackListSerializer

    def post(self, request):
        serializer = self.get_serializer()
        data = serializer.validate(attrs=request.data)
        token = RefreshToken(data.get('refresh'))
        self.check_user_permission(user_id=request.user.id, requested_id=token.payload["user_id"])
        token.blacklist()
        return Response({"message": "Success"}, status.HTTP_200_OK)

    @staticmethod
    def check_user_permission(user_id, requested_id):
        if user_id != requested_id:
            raise PermissionDenied("You do not have permission to logout another user")


class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == "resend_activation":
            return CustomResendActivationEmailSerializer
        return super().get_serializer_class()
