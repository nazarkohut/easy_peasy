from datetime import datetime, timedelta

import cloudinary.utils
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from easy_peasy import settings


class Cloudinary(generics.RetrieveAPIView):
    queryset = None
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        signature_expiration = 3
        time_now = datetime.now()
        hour_ago = time_now - timedelta(hours=1)
        calculated_timestamp = (hour_ago + timedelta(minutes=signature_expiration)).timestamp()
        signature = cloudinary.utils.api_sign_request({
            "timestamp": calculated_timestamp,
            "upload_preset": "easy_peasy",
        }, settings.CLOUDINARY_STORAGE['API_SECRET'])
        return Response(
            {"API_KEY": settings.CLOUDINARY['API_KEY'], "signature": signature, "timestamp": calculated_timestamp})
