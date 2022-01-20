from json import JSONDecodeError

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.fields import get_error_detail


def exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(detail=get_error_detail(exc))
    if isinstance(exc, JSONDecodeError):
        exc = DRFValidationError(detail={"message": "JSON is not valid"})
    return drf_exception_handler(exc, context)
