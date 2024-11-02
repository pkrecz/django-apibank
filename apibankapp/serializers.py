# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import CustomerModel, ParameterModel, AccountModel, AccountTypeModel, OperationModel, LogModel


""" Customer """
class CustomerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerModel
        fields = '__all__'
        read_only_fields = ['created_date', 'created_employee', 'avatar']


class CustomerUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerModel
        fields = '__all__'
        read_only_fields = ['created_date', 'created_employee']


class CustomerLRDSerializer(serializers.ModelSerializer):

    customer_accounts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='accounts-detail')

    class Meta:
        model = CustomerModel
        fields = [
                    'id_customer', 'first_name', 'last_name',
                    'street', 'house', 'apartment', 'postal_code', 'city',
                    'pesel', 'birth_date', 'birth_city', 'identification', 'avatar',
                    'created_date', 'created_employee', 'customer_accounts']


""" Account """
class AccountCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountModel
        fields = [
                    'debit', 'free_balance', 'percent',
                    'account_type', 'customer']
        read_only_fields = [
                            'free_balance']


class AccountUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountModel
        fields = [
                    'balance', 'debit', 'percent']
        read_only_fields = ['balance']


class AccountUpdateSecureSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountModel
        fields = [
                    'debit', 'free_balance', 'percent']


class AccountLRDSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountModel
        fields = [
                    'id_account', 'number_iban',
                    'balance', 'debit', 'free_balance', 'percent',
                    'created_date', 'created_employee',
                    'account_type', 'customer']
        depth = 1


class AccountOperationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountModel
        fields = [
                    'balance', 'free_balance', 'debit']


""" Account Type """
class AccountTypeCLRDSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountTypeModel
        fields = [
                    'id_account_type',
                    'code', 'description', 'subaccount', 'percent']


class AccountTypeUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountTypeModel
        fields = [
                    'description', 'subaccount', 'percent']


""" Operation """
class OperationNewSerializer(serializers.ModelSerializer):

    type_choice = [
                    ('', '--------'),
                    (1, 'Deposit'),
                    (2, 'Withdrawal')]
    type_operation = serializers.ChoiceField(choices=type_choice)

    class Meta:
        model = OperationModel
        fields = [
                    'type_operation', 'value_operation']


class OperationHistorySerializer(serializers.ModelSerializer):

    type_operation = serializers.CharField(source='get_type_operation_display')

    class Meta:
        model = OperationModel
        fields = [
                    'id_operation', 'type_operation',
                    'value_operation', 'balance_after_operation',
                    'operation_date', 'operation_employee']


class OperationInterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = OperationModel
        fields = [
                    'type_operation', 'value_operation',
                    'balance_after_operation', 'id_account']


""" Parameter """
class ParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParameterModel
        fields = '__all__'


""" Log monitoring """
class LogMonitoringSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogModel
        fields = '__all__'
