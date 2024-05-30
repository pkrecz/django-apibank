# -*- coding: utf-8 -*-

import os
from django.conf import settings
from django.db import models
from django.core.validators import (RegexValidator, MinValueValidator)


"""
Customer Model
"""
class CustomerModel(models.Model):

    def get_upload_path(instance, filename):
        dir_to_clear = os.path.join(settings.MEDIA_ROOT, 'image', 'avatar', str(instance.pk))
        if os.path.exists(dir_to_clear):
            files_to_remove = [os.path.join(dir_to_clear,f) for f in os.listdir(dir_to_clear)]
            for f in files_to_remove:
                os.remove(f)
        return os.path.join('image', 'avatar', str(instance.pk), filename)

    id_customer = models.AutoField(
                                primary_key=True)
    first_name = models.CharField(
                                max_length=100)
    last_name = models.CharField(
                                max_length=100)
    address = models.CharField(
                                max_length=100)
    postal_code = models.CharField(
                                max_length=6,
                                validators=[RegexValidator(regex='^[0-9]{2}-[0-9]{3}$')])
    city = models.CharField(
                                max_length=100)
    pesel = models.CharField(
                                max_length=11,
                                validators=[RegexValidator(regex='^[0-9]{11}$')])
    birth_date = models.DateField()
    birth_city = models.CharField(
                                max_length=100)
    identification = models.CharField(
                                max_length=9)
    avatar = models.ImageField(
                                upload_to=get_upload_path, blank=True, null=True)
    created_date = models.DateTimeField(
                                auto_now_add=True)
    created_employee = models.CharField(
                                max_length=50)

    def save(self, *args, **kwargs):
        self.identification = self.identification.upper()
        super().save(*args, **kwargs)


"""
Account Model
"""
class AccountModel(models.Model):

    id_account = models.AutoField(
                                primary_key=True)
    number_iban = models.CharField(
                                max_length=28,
                                blank=True)
    balance = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                default=0)
    debit = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                default=0,
                                validators=[MinValueValidator(0)])
    free_balance = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                default=0)
    percent = models.DecimalField(
                                max_digits=4,
                                decimal_places=2,
                                default=0,
                                validators=[MinValueValidator(0)])
    created_date = models.DateTimeField(
                                auto_now_add=True)
    created_employee = models.CharField(
                                max_length=50)

    account_type = models.ForeignKey('AccountTypeModel', on_delete=models.PROTECT)
    customer = models.ForeignKey('CustomerModel', related_name='Account', on_delete=models.PROTECT)


"""
AccountType Model
"""
class AccountTypeModel(models.Model):

    id_account_type = models.AutoField(
                                primary_key=True)
    code = models.CharField(
                                unique=True,
                                max_length=4,
                                validators=[RegexValidator(regex='^[a-zA-Z]{1}-[0-9]{2}$')])
    description = models.CharField(
                                max_length=100)
    subaccount = models.CharField(
                                max_length=6,
                                validators=[RegexValidator(regex='^[0-9]{6}$')])
    percent = models.DecimalField(
                                max_digits=4,
                                decimal_places=2,
                                default=0,
                                validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)


"""
Parameter Model
"""
class ParameterModel(models.Model):

    id_parameter = models.AutoField(
                                primary_key=True)
    country_code = models.CharField(
                                max_length=2,
                                validators=[RegexValidator(regex='^[a-zA-Z]{2}$')])
    bank_number = models.CharField(
                                max_length=8,
                                validators=[RegexValidator(regex='^[0-9]{8}$')])

    def save(self, *args, **kwargs):
        self.country_code = self.country_code.upper()
        super().save(*args, **kwargs)


"""
Operation Model
"""
class OperationModel(models.Model):

    type_choice = [
                    ('', '--------'),
                    (1, 'Deposit'),
                    (2, 'Withdrawal')]

    id_operation = models.AutoField(
                                primary_key=True)
    type_operation = models.IntegerField(
                                choices=type_choice)
    value_operation = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                default=0)
    balance_after_operation = models.DecimalField(
                                max_digits=12,
                                decimal_places=2)
    operation_date = models.DateTimeField(
                                auto_now_add=True)
    operation_employee = models.CharField(
                                max_length=50)
    
    id_account = models.ForeignKey('AccountModel', on_delete=models.PROTECT)
