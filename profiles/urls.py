from django.urls import path

from profiles.views import ProfileView, EditProfileView, ChangePassword

urlpatterns = [
    path('<user_id>/', ProfileView.as_view(), name='profile'),
    path('edit/<int:pk>/', EditProfileView.as_view(), name='edit'),
    path('change_password/<int:pk>/', ChangePassword.as_view(), name='change_password')
]

