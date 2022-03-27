from django.urls import path

# from users.serializers import CustomTokenObtainPairSerializer
from users.views import RegisterView, BlacklistRefreshView, CustomTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", BlacklistRefreshView.as_view(), name="logout"),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
