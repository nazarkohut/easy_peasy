from django.urls import path

from profiles.views import ProfileView, EditProfileView

urlpatterns = [
    path('<user_id>/', ProfileView.as_view(), name='profile'),
    path('edit/<int:pk>/', EditProfileView.as_view(), name='edit')
]

