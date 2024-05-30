from rest_framework import serializers
from .models import (CustomerModel, ParameterModel, AccountModel, AccountTypeModel, OperationModel)


"""
Customized class
"""
class HyperlinkedGenerate(serializers.HyperlinkedIdentityField):
    
    def get_url(self, *args):
        url = super().get_url(*args)
        return url + 'generate/'


"""
Customer
"""
class CustomerCreateSerializer(serializers.HyperlinkedModelSerializer):
    """
    Actions: create
    """

    class Meta:
        model = CustomerModel
        fields = '__all__'
        read_only_fields = ('created_date', 'created_employee', 'avatar')


class CustomerUpdateSerializer(serializers.HyperlinkedModelSerializer):
    """
    Actions: update & partial_udpate
    """

    class Meta:
        model = CustomerModel
        fields = '__all__'
        read_only_fields = ('created_date', 'created_employee')


class CustomerLRDSerializer(serializers.HyperlinkedModelSerializer):
    """
    Actions: list & retrieve & destroy
    """
    account = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='accountmodel-detail')
            
    class Meta:
        model = CustomerModel
        fields = [
                    'url', 'first_name', 'last_name',
                    'address', 'postal_code', 'city',
                    'pesel', 'birth_date', 'birth_city', 'identification', 'avatar',
                    'created_date', 'created_employee', 'account']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['full_name'] = instance.first_name + ' ' + instance.last_name
        return representation


"""
Account
"""
class AccountCreateSerializer(serializers.HyperlinkedModelSerializer):
    """
    Actions: create
    """

    class Meta:
        model = AccountModel
        fields = [
                    'url', 'number_iban',
                    'balance', 'debit', 'free_balance', 'percent',
                    'created_date', 'created_employee',
                    'account_type', 'customer']
        read_only_fields = (
                            'number_iban', 'balance', 'free_balance',
                            'created_date', 'created_employee')


class AccountUPSerializer(serializers.HyperlinkedModelSerializer):
    """
    Actions: update & partial_udpate
    """

    class Meta:
        model = AccountModel
        fields = [
                    'url', 'number_iban',
                    'balance', 'debit', 'free_balance', 'percent',
                    'created_date', 'created_employee',
                    'account_type', 'customer']
        read_only_fields = (
                            'number_iban', 'balance', 'free_balance',
                            'created_date', 'created_employee',
                            'account_type', 'customer')
    
    def validate_free_balance(self, value):
        if value < 0:
            raise serializers.ValidationError('Free balance out of limit!')
        return value
    
    def validate_number_iban(self, value):
        if len(value) != 28:
            raise serializers.ValidationError('IBAN should have 28 characters!')
        return value


class AccountLRDSerializer(serializers.HyperlinkedModelSerializer):
    """
    Actions: list & retrieve & destroy
    """
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
    """
    Action: Update data after transaction
    """

    class Meta:
        model = AccountModel
        fields = [
                    'balance', 'free_balance', 'debit']

    def validate_free_balance(self, value):
        if value < 0:
            raise serializers.ValidationError('Value operation out of balance limit!')
        return value


"""
Account Type
"""
class AccountTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AccountTypeModel
        fields = '__all__'


"""
Parameter
"""
class ParameterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ParameterModel
        fields = '__all__'


"""
Operation
"""
class OperationNewSerializer(serializers.HyperlinkedModelSerializer):
    """
    Actions: new operation for account
    """

    class Meta:
        model = OperationModel
        fields = '__all__'
        read_only_fields = ('id_operation', 'balance_after_operation', 'operation_date', 'operation_employee', 'id_account')


class OperationHistorySerializer(serializers.HyperlinkedModelSerializer):
    """
    Actions: list of history
    """
    type_operation = serializers.CharField(source='get_type_operation_display')

    class Meta:
        model = OperationModel
        fields = [
                    'id_operation', 'type_operation',
                    'value_operation', 'balance_after_operation',
                    'operation_date', 'operation_employee']
