# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError


class CustomerModel(models.Model):
    """ Customer Model """

    id_customer = models.AutoField(
                                primary_key=True,
                                verbose_name='Id customer')
    first_name = models.CharField(
                                max_length=100,
                                verbose_name='First name')
    last_name = models.CharField(
                                max_length=100,
                                verbose_name='Last name')
    address = models.CharField(
                                max_length=100,
                                verbose_name='Address')
    postal_code = models.CharField(
                                max_length=6,
                                validators=[RegexValidator(regex='^[0-9]{2}-[0-9]{3}$')],
                                verbose_name='Postal code')
    city = models.CharField(
                                max_length=100,
                                verbose_name='City')
    pesel = models.CharField(
                                max_length=11,
                                validators=[RegexValidator(regex='^[0-9]{11}$')],
                                verbose_name='PESEL')
    birth_date = models.DateField(
                                verbose_name='Birth day')
    birth_city = models.CharField(
                                max_length=100,
                                verbose_name='Birth city')
    identification = models.CharField(
                                max_length=9,
                                verbose_name='Identification')
    created_date = models.DateTimeField(
                                auto_now_add=True,
                                verbose_name='Created date')
    created_employee = models.CharField(
                                max_length=50,
                                verbose_name='Employee')

    def save(self, *args, **kwargs):
        self.identification = self.identification.upper()
        super().save(*args, **kwargs)


class AccountModel(models.Model):
    """ Account Model """

    id_account = models.AutoField(
                                primary_key=True,
                                verbose_name='Id account')
    number_iban = models.CharField(
                                max_length=28,
                                blank=True,
                                verbose_name='IBAN number')
    balance = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                default=0,
                                verbose_name='Balance')
    debit = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                default=0,
                                validators=[MinValueValidator(0)],
                                verbose_name='Debit')
    free_balance = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                default=0,
                                verbose_name='Free balance')
    percent = models.DecimalField(
                                max_digits=4,
                                decimal_places=2,
                                default=0,
                                validators=[MinValueValidator(0)],
                                verbose_name='Percent')
    created_date = models.DateTimeField(
                                auto_now_add=True,
                                verbose_name='Created date')
    created_employee = models.CharField(
                                max_length=50,
                                verbose_name='Employee')

    account_type = models.ForeignKey('AccountTypeModel', on_delete=models.PROTECT)
    customer = models.ForeignKey('CustomerModel', related_name='Account', on_delete=models.PROTECT)

    def clean(self):
        if self.free_balance < 0:
            raise ValidationError({'Free balance': ['Value operation out of limit.']})


class AccountTypeModel(models.Model):
    """ AccountType Model """

    id_account_type = models.AutoField(
                                primary_key=True,
                                verbose_name='Id account type')
    code = models.CharField(
                                unique=True,
                                max_length=4,
                                verbose_name='Code',
                                validators=[RegexValidator(regex='^[a-zA-Z]{1}-[0-9]{2}$')])
    description = models.CharField(
                                max_length=100,
                                verbose_name='Description')
    subaccount = models.CharField(
                                max_length=6,
                                verbose_name='Subaccount',
                                validators=[RegexValidator(regex='^[0-9]{6}$')])
    percent = models.DecimalField(
                                max_digits=4,
                                decimal_places=2,
                                default=0,
                                verbose_name='Percent',
                                validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)


class ParameterModel(models.Model):
    """ Parameter Model """

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


class OperationModel(models.Model):
    """ Operation Model """

    type_choice = [
                    ('', '--------'),
                    (1, 'Deposit'),
                    (2, 'Withdrawal')]

    id_operation = models.AutoField(
                                primary_key=True,
                                verbose_name='Id operation')
    type_operation = models.IntegerField(
                                choices=type_choice,
                                verbose_name='Type operation')
    value_operation = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                default=0,
                                verbose_name='Value operation')
    balance_after_operation = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                verbose_name='Balance after operation')
    operation_date = models.DateTimeField(
                                auto_now_add=True,
                                verbose_name='Operation date')
    operation_employee = models.CharField(
                                max_length=50,
                                verbose_name='Employee')
    
    id_account = models.ForeignKey('AccountModel', on_delete=models.PROTECT)
