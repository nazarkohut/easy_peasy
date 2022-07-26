from django.urls import path

from profiles.views import ProfileView

urlpatterns = [
    path('<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('', ProfileView.as_view(), name='edit'),
]
