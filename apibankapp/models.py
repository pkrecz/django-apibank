# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError


class CustomerModel(models.Model):
    """ Customer Model """

    Id_customer = models.AutoField(
                                primary_key=True,
                                verbose_name='Id customer')
    First_name = models.CharField(
                                max_length=100,
                                verbose_name='First name')
    Last_name = models.CharField(
                                max_length=100,
                                verbose_name='Last name')
    Address = models.CharField(
                                max_length=100,
                                verbose_name='Address')
    Postal_code = models.CharField(
                                max_length=6,
                                validators=[RegexValidator(regex='^[0-9]{2}-[0-9]{3}$')],
                                verbose_name='Postal code')
    City = models.CharField(
                                max_length=100,
                                verbose_name='City')
    Pesel = models.CharField(
                                max_length=11,
                                validators=[RegexValidator(regex='^[0-9]{11}$')],
                                verbose_name='PESEL')
    Birth_date = models.DateField(
                                verbose_name='Birth day')
    Birth_city = models.CharField(
                                max_length=100,
                                verbose_name='Birth city')
    Identification = models.CharField(
                                max_length=9,
                                verbose_name='Identification')
    Created_date = models.DateTimeField(
                                auto_now_add=True,
                                verbose_name='Created date')
    Created_employee = models.CharField(
                                max_length=50,
                                verbose_name='Employee')

    def save(self, *args, **kwargs):
        self.Identification = self.Identification.upper()
        super().save(*args, **kwargs)


class AccountModel(models.Model):
    """ Account Model """

    Id_account = models.AutoField(
                                primary_key=True,
                                verbose_name='Id account')
    Number_IBAN = models.CharField(
                                max_length=28,
                                blank=True,
                                verbose_name='IBAN number')
    Balance = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                default=0,
                                verbose_name='Balance')
    Debit = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                default=0,
                                validators=[MinValueValidator(0)],
                                verbose_name='Debit')
    Free_balance = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                default=0,
                                verbose_name='Free balance')
    Percent = models.DecimalField(
                                max_digits=4,
                                decimal_places=2,
                                default=0,
                                validators=[MinValueValidator(0)],
                                verbose_name='Percent')
    Created_date = models.DateTimeField(
                                auto_now_add=True,
                                verbose_name='Created date')
    Created_employee = models.CharField(
                                max_length=50,
                                verbose_name='Employee')

    Account_type = models.ForeignKey('AccountTypeModel', on_delete=models.PROTECT)
    Customer = models.ForeignKey('CustomerModel', related_name='Account', on_delete=models.PROTECT)

    def clean(self):
        if self.Free_balance < 0:
            raise ValidationError({'Free balance': ['Value operation out of limit.']})


class AccountTypeModel(models.Model):
    """ AccountType Model """

    Id_account_type = models.AutoField(
                                primary_key=True,
                                verbose_name='Id account type')
    Code = models.CharField(
                                unique=True,
                                max_length=4,
                                verbose_name='Code',
                                validators=[RegexValidator(regex='^[a-zA-Z]{1}-[0-9]{2}$')])
    Description = models.CharField(
                                max_length=100,
                                verbose_name='Description')
    Subaccount = models.CharField(
                                max_length=6,
                                verbose_name='Subaccount',
                                validators=[RegexValidator(regex='^[0-9]{6}$')])
    Percent = models.DecimalField(
                                max_digits=4,
                                decimal_places=2,
                                default=0,
                                verbose_name='Percent',
                                validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        self.Code = self.Code.upper()
        super().save(*args, **kwargs)


class ParameterModel(models.Model):
    """ Parameter Model """

    Id_parameter = models.AutoField(
                                primary_key=True)
    Country_code = models.CharField(
                                max_length=2,
                                validators=[RegexValidator(regex='^[a-zA-Z]{2}$')])
    Bank_number = models.CharField(
                                max_length=8,
                                validators=[RegexValidator(regex='^[0-9]{8}$')])

    def save(self, *args, **kwargs):
        self.Country_code = self.Country_code.upper()
        super().save(*args, **kwargs)


class OperationModel(models.Model):
    """ Operation Model """

    type_choice = [
                    ('', '--------'),
                    (1, 'Deposit'),
                    (2, 'Withdrawal')]

    Id_operation = models.AutoField(
                                primary_key=True,
                                verbose_name='Id operation')
    Type_operation = models.IntegerField(
                                choices=type_choice,
                                verbose_name='Type operation')
    Value_operation = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                default=0,
                                verbose_name='Value operation')
    Balance_after_operation = models.DecimalField(
                                max_digits=12,
                                decimal_places=2,
                                verbose_name='Balance after operation')
    Operation_date = models.DateTimeField(
                                auto_now_add=True,
                                verbose_name='Operation date')
    Operation_employee = models.CharField(
                                max_length=50,
                                verbose_name='Employee')
    
    Id_account = models.ForeignKey('AccountModel', on_delete=models.PROTECT)
