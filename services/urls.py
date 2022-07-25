from django.urls import path

from services.views import Cloudinary

urlpatterns = [
    path('cloudinary/', Cloudinary.as_view(), name='cloudinary')
]
