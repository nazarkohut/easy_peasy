from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import EmailTokenObtainPairSerializer, UsernameTokenObtainPairSerializer, BlackListSerializer


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
        token.blacklist()
        return Response({"message": "Success"}, status.HTTP_200_OK)
