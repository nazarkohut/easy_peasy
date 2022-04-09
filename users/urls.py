from django.urls import path

from users.views import BlacklistRefreshView, CustomTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("logout/", BlacklistRefreshView.as_view(), name="logout"),
    path('users/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
