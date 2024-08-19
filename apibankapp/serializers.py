# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import (CustomerModel, ParameterModel, AccountModel, AccountTypeModel, OperationModel, LogModel)


""" Customized class """
class HyperlinkedGenerate(serializers.HyperlinkedIdentityField):
    
    def get_url(self, *args):
        url = super().get_url(*args)
        return url + 'generate/'


""" Customer """
class CustomerCreateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomerModel
        fields = '__all__'
        read_only_fields = ['created_date', 'created_employee', 'avatar']


class CustomerUpdateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomerModel
        fields = '__all__'
        read_only_fields = ['created_date', 'created_employee']


class CustomerLRDSerializer(serializers.HyperlinkedModelSerializer):

    account = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='accountmodel-detail')
            
    class Meta:
        model = CustomerModel
        fields = [
                    'url', 'first_name', 'last_name',
                    'street', 'house', 'apartment', 'postal_code', 'city',
                    'pesel', 'birth_date', 'birth_city', 'identification', 'avatar',
                    'created_date', 'created_employee', 'account']


""" Account """
class AccountCreateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AccountModel
        fields = [
                    'debit', 'free_balance', 'percent',
                    'account_type', 'customer']
        read_only_fields = [
                            'free_balance']


class AccountUpdateSerializer(serializers.HyperlinkedModelSerializer):

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


class AccountLRDSerializer(serializers.HyperlinkedModelSerializer):

    generate_link = HyperlinkedGenerate(view_name='accountmodel-detail')

    class Meta:
        model = AccountModel
        fields = [
                    'url', 'number_iban', 'generate_link',
                    'balance', 'debit', 'free_balance', 'percent',
                    'created_date', 'created_employee',
                    'account_type', 'customer']
        depth = 1


class AccountOperationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AccountModel
        fields = [
                    'balance', 'free_balance', 'debit']


""" Account Type """
class AccountTypeCLRDSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AccountTypeModel
        fields = '__all__'


class AccountTypeUpdateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AccountTypeModel
        fields = [
                    'description', 'subaccount', 'percent']


""" Parameter """
class ParameterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ParameterModel
        fields = '__all__'


""" Operation """
class OperationNewSerializer(serializers.HyperlinkedModelSerializer):

    type_choice = [
                    ('', '--------'),
                    (1, 'Deposit'),
                    (2, 'Withdrawal')]
    type_operation = serializers.ChoiceField(choices=type_choice)

    class Meta:
        model = OperationModel
        fields = [
                    'type_operation', 'value_operation']


class OperationHistorySerializer(serializers.HyperlinkedModelSerializer):

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


""" Log monitoring """
class LogMonitoringSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogModel
        fields = '__all__'
