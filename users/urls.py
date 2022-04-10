from django.urls import path

from users.views import BlacklistRefreshView, CustomTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("users/logout/", BlacklistRefreshView.as_view(), name="logout"),
    path('users/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
