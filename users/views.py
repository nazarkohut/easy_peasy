from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import EmailTokenObtainPairSerializer, UsernameTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    def get_serializer_class(self):
        if "email" in self.request.data:
            return EmailTokenObtainPairSerializer
        return UsernameTokenObtainPairSerializer


class BlacklistRefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success", status.HTTP_200_OK)
