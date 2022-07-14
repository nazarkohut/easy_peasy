from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import BlacklistRefreshView, CustomTokenObtainPairView, CustomUserViewSet

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r"users", CustomUserViewSet)

urlpatterns = [
    path("users/logout/", BlacklistRefreshView.as_view(), name="logout"),
    path('users/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('users/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^', include(router.urls))
]
