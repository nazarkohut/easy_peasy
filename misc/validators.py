"""This file contains custom validation methods"""
from collections import defaultdict, Counter

from rest_framework.exceptions import ValidationError


def find_missing(fields: dict, data: dict) -> dict:
    missing = defaultdict(list)
    for field in fields:
        if field not in data:
            missing[field].append("Field is required")
    return missing


def check_fields(fields: list, data: dict):
    for field in fields:
        if field not in data:
            raise ValidationError({"message": "request body is not valid", "details": f"{field} is required"})


def simple_email_validation(email):
    """This function is not main for email validation; it is intended to better user experience"""
    c = Counter(email)
    if c['@'] != 1:
        raise ValidationError("Email should contain '@' sign")
