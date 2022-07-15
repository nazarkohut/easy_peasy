from django.urls import path

from profiles.views import ProfileView, ChangePassword

urlpatterns = [
    path('<int:user_id>/', ProfileView.as_view(), name='edit'),
    path('', ProfileView.as_view(), name='profile'),
    path('change_password/<int:pk>/', ChangePassword.as_view(), name='change_password')
]
