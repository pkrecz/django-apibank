from rest_framework import viewsets
from rest_framework import status
from rest_framework import filters 
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import (MultiPartParser, FormParser, JSONParser)
from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from collections import OrderedDict
from django.db.models import ProtectedError
from .models import (CustomerModel, AccountModel, AccountTypeModel, ParameterModel, OperationModel)
from .serializers import (
                            CustomerCreateSerializer, CustomerUpdateSerializer, CustomerLRDSerializer,
                            AccountCreateSerializer, AccountUpdateSerializer, AccountLRDSerializer, AccountOperationSerializer,
                            AccountTypeSerializer,
                            ParameterSerializer,
                            OperationNewSerializer, OperationHistorySerializer)


"""
Customized class
"""
class AccountTypeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name='code', lookup_expr="istartswith")


"""
Customer
"""
class CustomerViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    queryset = CustomerModel.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['pesel', 'identification']
    ordering_fields = ['last_name']
       
    def get_serializer_class(self):
        match self.action:
            case 'create':
                return CustomerCreateSerializer
            case 'update' | 'partial_update':
                return CustomerUpdateSerializer
            case _:
                return CustomerLRDSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({'message': 'You can not delete this record!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        serializer.validated_data['created_employee'] = self.request.user
        return serializer.save()


"""
Account
"""
class AccountViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = AccountModel.objects.all()

    def get_serializer_class(self):
        match self.action:
            case 'newoperation':
                return OperationNewSerializer
            case 'create':
                return AccountCreateSerializer
            case 'update' | 'partial_update':
                return AccountUpdateSerializer
            case _:
                return AccountLRDSerializer

    def create(self, request, *args, **kwargs):
        data = OrderedDict(request.data)
        data['free_balance'] = data['debit']
        serializer = self.get_serializer(data=data)
        serializer.fields['free_balance'].read_only = False
        serializer.is_valid(raise_exception=True)
        serializer.fields['free_balance'].read_only = True
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('debit', None) is not None:
            data = OrderedDict(request.data)
            data['free_balance'] = str(round(float(data['debit']) + float(instance.balance), 2))
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.fields['free_balance'].read_only = False
            serializer.is_valid(raise_exception=True)
            serializer.fields['free_balance'].read_only = True
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({'message': 'You can not delete this record!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        serializer.validated_data['created_employee'] = self.request.user
        return serializer.save()

    @action(detail=True, methods=['get'])
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
            # Updating IBAN
            serializer = AccountLRDSerializer(instance, data={'number_iban': iban}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(AccountLRDSerializer(instance, context={'request': request}).data)
        else:
            return Response({'message': 'IBAN number already exists.'})

    @transaction.atomic
    @action(detail=True, methods=['get', 'post'])
    def newoperation(self, request, pk=None):
        instance = self.get_object()
        if request.method == 'POST': 
            serializer = OperationNewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Operation type
            if serializer.validated_data['type_operation'] == 2:
                serializer.validated_data['value_operation'] = serializer.validated_data['value_operation'] * (-1)
            # Data from AccountModel
            balance = AccountModel.objects.get(id_account=instance.id_account).balance
            debit = AccountModel.objects.get(id_account=instance.id_account).debit
            # Set up balance & free_balance after transaction
            balance_after_operation = balance + serializer.validated_data['value_operation']
            free_balance_after_operation = balance_after_operation + debit
            # Updating balance & free balance for AccountModel
            data = {
                    'balance': balance_after_operation,
                    'free_balance': free_balance_after_operation}
            serializer_account = AccountOperationSerializer(instance, data=data, partial=True)
            serializer_account.is_valid(raise_exception=True)
            serializer_account.save()
            # New object in OperationModel
            serializer.validated_data['id_account'] = instance
            serializer.validated_data['balance_after_operation'] = balance_after_operation
            serializer.validated_data['operation_employee'] = self.request.user
            serializer.save()
        return Response(AccountLRDSerializer(instance, context={'request': request}).data)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        instance = self.get_object()
        queryset = OperationModel.objects.filter(id_account=instance.id_account).order_by('-operation_date')
        serializer = OperationHistorySerializer(queryset, context={'request': request}, many=True)
        return Response(data=serializer.data)
    
    @action(detail=False, methods=['get'])
    def interest(self, request, pk=None):
        data = AccountModel.objects.filter(balance__gt = 0, percent__gt = 0)
        if data.exists():
            with transaction.atomic():
                counter = 0
                for instance in data:
                    interest = round(instance.balance * (instance.percent / 100),2)
                    new_balance = instance.balance + interest
                    new_free_balance = new_balance + instance.debit
                    # Updating balance & free balance
                    AccountModel.objects.filter(id_account=instance.id_account).update(balance=new_balance, free_balance=new_free_balance)
                    # New object in OperationModel
                    OperationModel.objects.create(type_operation = 3, value_operation = interest, balance_after_operation = new_balance, id_account = instance)
                    counter += 1
                msg = 'Interest for ' + str(counter) + ' account(s) has been recounted.'
                return Response({'message': msg})
        else:
            return Response({'message': 'No accounts to be recounted.'})


"""
Account Type
"""
class AccountTypeViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    queryset = AccountTypeModel.objects.all()
    serializer_class = AccountTypeSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = AccountTypeFilter
    ordering_fields = ['code']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({'message': 'You can not delete this record!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
Parameter
"""
class ParameterViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'put']
    queryset = ParameterModel.objects.all()
    serializer_class = ParameterSerializer
