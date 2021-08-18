from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.serializers import UserSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status.HTTP_201_CREATED)

