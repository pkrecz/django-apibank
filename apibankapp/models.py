# -*- coding: utf-8 -*-

import os
import uuid
from decimal import Decimal
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from .validators import validator_free_balance, validator_number_iban, validator_file_size


""" Customer Model """
class CustomerModel(models.Model):

    def get_upload_path(instance, filename):
        file_name = uuid.uuid4().hex
        file_extension = filename.split('.').pop()
        file_name_full = f"{file_name}.{file_extension}"
        file_path = os.path.join("image", "avatars", file_name_full)
        return file_path

    id_customer = models.AutoField(
                                primary_key=True)
    first_name = models.CharField(
                                max_length=100)
    last_name = models.CharField(
                                max_length=100)
    street = models.CharField(
                                max_length=100)
    house = models.CharField(
                                max_length=10)
    apartment = models.CharField(
                                blank=True,
                                max_length=10)
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
                                upload_to=get_upload_path,
                                blank=True,
                                null=True,
                                validators=[validator_file_size])
    created_date = models.DateTimeField(
                                auto_now_add=True)
    created_employee = models.CharField(
                                max_length=50)

    def save(self, *args, **kwargs):
        self.identification = self.identification.upper()
        super().save(*args, **kwargs)


""" Account Model """
class AccountModel(models.Model):

    id_account = models.AutoField(
                                primary_key=True)
    number_iban = models.CharField(
                                max_length=28,
                                blank=True,
                                validators=[validator_number_iban])
    balance = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                default=0)
    debit = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                validators=[MinValueValidator(Decimal(0))])
    free_balance = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                validators=[validator_free_balance])
    percent = models.DecimalField(
                                max_digits=4,
                                decimal_places=2,
                                validators=[MinValueValidator(Decimal(0))])
    created_date = models.DateTimeField(
                                auto_now_add=True)
    created_employee = models.CharField(
                                max_length=50)

    account_type = models.ForeignKey("AccountTypeModel", related_name="accounttype_accounts", on_delete=models.PROTECT)
    customer = models.ForeignKey("CustomerModel", related_name="customer_accounts", on_delete=models.PROTECT)


""" AccountType Model """
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
                                validators=[MinValueValidator(Decimal(0))])

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)


""" Parameter Model """
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


""" Operation Model """
class OperationModel(models.Model):

    type_choice = [
                    ("", "--------"),
                    (1, "Deposit"),
                    (2, "Withdrawal"),
                    (3, "Interest")]

    id_operation = models.AutoField(
                                primary_key=True)
    type_operation = models.IntegerField(
                                choices=type_choice)
    value_operation = models.DecimalField(
                                max_digits=12,
                                decimal_places=2)
    balance_after_operation = models.DecimalField(
                                max_digits=12,
                                decimal_places=2)
    operation_date = models.DateTimeField(
                                auto_now_add=True)
    operation_employee = models.CharField(
                                max_length=50)
    
    id_account = models.ForeignKey("AccountModel", related_name="account_operations", on_delete=models.PROTECT)


""" Log Model """
class LogModel(models.Model):
    
    id_log = models.AutoField(
                                primary_key=True)
    date_log = models.DateTimeField(
                                auto_now_add=True)
    action_log = models.CharField(
                                max_length=50)
    function_log = models.CharField(
                                max_length=50)
    duration_log = models.DecimalField(
                                max_digits=12,
                                decimal_places=6)
    data_log = models.CharField(
                                max_length=250,
                                blank=True)
    user_log = models.CharField(
                                max_length=50)
    status_log = models.CharField(
                                max_length=20)
