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
        read_only_fields = ('Created_date', 'Created_employee')


class CustomerLRDSerializer(serializers.HyperlinkedModelSerializer):
    """ Actions: list & retrieve & destroy """

    Account = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='accountmodel-detail')
            
    class Meta:
        model = CustomerModel
        fields = [
                    'url', 'First_name', 'Last_name',
                    'Address', 'Postal_code', 'City',
                    'Pesel', 'Birth_date', 'Birth_city', 'Identification',
                    'Created_date', 'Created_employee', 'Account']

    def to_representation(self, instance):
        
        representation = super().to_representation(instance)
        representation['Full_name'] = instance.First_name + ' ' + instance.Last_name
        return representation


""" Account """
class AccountCUPSerializer(serializers.HyperlinkedModelSerializer):
    """ Actions: create & update & partial_udpate """

    class Meta:
        model = AccountModel
        fields = '__all__'
        read_only_fields = ('Number_IBAN', 'Balance', 'Free_balance', 'Created_date', 'Created_employee')


class AccountLRDSerializer(serializers.HyperlinkedModelSerializer):
    """ Actions: list & retrieve & destroy """

    Generate_link = HyperlinkedGenerate(view_name='accountmodel-detail')

    class Meta:
        model = AccountModel
        fields = [
                    'url', 'Number_IBAN', 'Generate_link',
                    'Balance', 'Debit', 'Free_balance', 'Percent',
                    'Created_date', 'Created_employee',
                    'Account_type', 'Customer']
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
