# -*- coding: utf-8 -*-

from rest_framework.exceptions import ValidationError


def validator_free_balance(value):
    if value < 0:
        raise ValidationError(detail={"message": "Free balance out of limit!"}, code=400)
    return value

def validator_number_iban(value):
    if len(value) != 28:
        raise ValidationError(detail={"message": "IBAN number should have 28 characters!"}, code=400)
    return value
