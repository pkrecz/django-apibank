from .models import CustomerModel, ParameterModel, AccountModel, AccountTypeModel
from rest_framework import serializers


""" Customized class """
class HyperlinkedGenerate(serializers.HyperlinkedIdentityField):
    
    def get_url(self, *args):
        url = super().get_url(*args)
        return url + 'generate/'


""" Customer """
class CustomerCUPSerializer(serializers.HyperlinkedModelSerializer):
    """ Actions: create & update & partial_udpate """

    class Meta:
        model = CustomerModel
        fields = '__all__'
        read_only_fields = ('created_date', 'created_employee')


class CustomerLRDSerializer(serializers.HyperlinkedModelSerializer):
    """ Actions: list & retrieve & destroy """

    account = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='accountmodel-detail')
            
    class Meta:
        model = CustomerModel
        fields = [
                    'url', 'first_name', 'last_name',
                    'address', 'postal_code', 'city',
                    'pesel', 'birth_date', 'birth_city', 'identification',
                    'created_date', 'created_employee', 'account']

    def to_representation(self, instance):
        
        representation = super().to_representation(instance)
        representation['full_name'] = instance.first_name + ' ' + instance.last_name
        return representation


""" Account """
class AccountCUPSerializer(serializers.HyperlinkedModelSerializer):
    """ Actions: create & update & partial_udpate """

    class Meta:
        model = AccountModel
        fields = '__all__'
        read_only_fields = ('number_iban', 'balance', 'free_balance', 'created_date', 'created_employee')


class AccountLRDSerializer(serializers.HyperlinkedModelSerializer):
    """ Actions: list & retrieve & destroy """

    generate_link = HyperlinkedGenerate(view_name='accountmodel-detail')

    class Meta:
        model = AccountModel
        fields = [
                    'url', 'number_iban', 'generate_link',
                    'balance', 'debit', 'free_balance', 'percent',
                    'created_date', 'created_employee',
                    'account_type', 'customer']
        depth = 1


""" Account Type """
class AccountTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AccountTypeModel
        fields = '__all__'


""" Parameter """
class ParameterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ParameterModel
        fields = '__all__'
