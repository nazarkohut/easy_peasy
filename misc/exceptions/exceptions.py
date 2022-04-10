from json import JSONDecodeError

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.fields import get_error_detail
from rest_framework_simplejwt import exceptions


def exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(detail=get_error_detail(exc))
    if isinstance(exc, JSONDecodeError):
        exc = DRFValidationError(detail={"message": "JSON is not valid"})
    if isinstance(exc, exceptions.TokenError):
        exc = DRFValidationError(detail={"message": "Token is invalid or expired"})
    return drf_exception_handler(exc, context)
