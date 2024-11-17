# -*- coding: utf-8 -*-

import os
from rest_framework.exceptions import ValidationError


def validator_free_balance(value):
    if value < 0:
        raise ValidationError(detail={"message": "Free balance out of limit!"}, code=400)
    return value


def validator_number_iban(value):
    if len(value) != 28:
        raise ValidationError(detail={"message": "IBAN number should have 28 characters!"}, code=400)
    return value


def validator_file_size(value):
    file_size = value.size
    limit_size_MB = float(os.getenv('MAX_IMAGE_FILE_SIZE_MB'))
    if file_size > limit_size_MB * 1024 * 1024:
        raise ValidationError(detail={"message": f"File size is too large. Limit is {limit_size_MB} MB."}, code=400)
    return value
