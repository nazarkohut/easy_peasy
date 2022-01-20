"""This file contains custom validation methods"""
from collections import defaultdict


def find_missing(fields: dict, data: dict) -> dict:
    missing = defaultdict(list)
    for field in fields:
        if field not in data:
            missing[field].append("Answer field is required")
    return missing
