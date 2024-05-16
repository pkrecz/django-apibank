from rest_framework import viewsets
from rest_framework import status
from rest_framework import filters 
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomerModel, AccountModel, AccountTypeModel, ParameterModel
from .serializers import (
                            CustomerCUPSerializer, CustomerLRDSerializer,
                            AccountCUPSerializer, AccountLRDSerializer,
                            AccountTypeSerializer,
                            ParameterSerializer)


""" Customized class """
class AccountTypeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name='code', lookup_expr="istartswith")



""" Customer """
class CustomerViewSet(viewsets.ModelViewSet):

    queryset = CustomerModel.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['pesel', 'identification']
    ordering_fields = ['last_name']
        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_udpate']:
            return CustomerCUPSerializer
        else:
            return CustomerLRDSerializer
    
    def perform_create(self, serializer):
            return serializer.save(created_employee=self.request.user)


""" Account """
class AccountViewSet(viewsets.ModelViewSet):

    queryset = AccountModel.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_udpate']:
            return AccountCUPSerializer
        else:
            return AccountLRDSerializer
    
    def perform_create(self, serializer):
            return serializer.save(created_employee=self.request.user)


    @action(detail=True, methods=['get', 'patch'])
    def generate(self, request, pk=None):

        instance = self.get_object()
        if not instance.number_iban:
            # Preparing IBAN
            account = str(instance.id_account)
            customer = str(instance.customer_id)
            country_code = ParameterModel.objects.get().country_code
            bank_number = ParameterModel.objects.get().bank_number
            subaccount = AccountTypeModel.objects.get(id_account_type=instance.account_type_id).subaccount
            prefix_zero = ''
            while len(customer) + len(account) + len(prefix_zero) < 12:
                prefix_zero = prefix_zero + '0'
            iban = country_code + bank_number + subaccount + account + prefix_zero + customer
            
            serializer = AccountLRDSerializer(instance, data={'number_iban': iban}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(AccountLRDSerializer(instance, context={'request': request}).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'IBAN number already exist.'})


""" Account Type """
class AccountTypeViewSet(viewsets.ModelViewSet):

    queryset = AccountTypeModel.objects.all()
    serializer_class = AccountTypeSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = AccountTypeFilter
    ordering_fields = ['code']


""" Parameter """
class ParameterViewSet(viewsets.ModelViewSet):

    queryset = ParameterModel.objects.all()
    serializer_class = ParameterSerializer
    http_method_names = ['get', 'put', 'patch']

