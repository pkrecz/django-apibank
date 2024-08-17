# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework import status
from rest_framework import filters 
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.parsers import (MultiPartParser, FormParser, JSONParser)
from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.db.models import ProtectedError
from collections import OrderedDict
from .models import (CustomerModel, AccountModel, AccountTypeModel, ParameterModel, OperationModel, LogModel)
from .serializers import (
                            CustomerCreateSerializer, CustomerUpdateSerializer, CustomerLRDSerializer,
                            AccountCreateSerializer, AccountUpdateSerializer, AccountLRDSerializer, AccountOperationSerializer, AccountUpdateSecureSerializer,
                            AccountTypeCLRDSerializer, AccountTypeUpdateSerializer,
                            ParameterSerializer,
                            OperationNewSerializer, OperationHistorySerializer, OperationInterestSerializer,
                            LogMonitoringSerializer)
from .decorators import ActivityMonitoringClass


""" Customized class """
class AccountTypeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name='code', lookup_expr="istartswith")


""" Customer """
class CustomerViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    queryset = CustomerModel.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['pesel', 'identification']
    ordering_fields = ['last_name']
       
    def get_serializer_class(self):
        match self.action:
            case 'create':
                return CustomerCreateSerializer
            case 'update':
                return CustomerUpdateSerializer
            case _:
                return CustomerLRDSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response({'message': 'Customer has been deleted.'}, status=status.HTTP_200_OK)
        except ProtectedError:
            return Response({'message': 'Deletion impossible. This record has referenced data!'}, status=status.HTTP_400_BAD_REQUEST)
        except APIException as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save(created_employee=self.request.user)
            return_serializer = CustomerLRDSerializer(instance, context={'request': request})
            return Response(return_serializer.data, status=status.HTTP_201_CREATED)
        except APIException as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)


""" Account """
class AccountViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = AccountModel.objects.all()

    def get_serializer_class(self):
        match self.action:
            case 'newoperation':
                return OperationNewSerializer
            case 'create':
                return AccountCreateSerializer
            case 'update':
                return AccountUpdateSerializer
            case _:
                return AccountLRDSerializer

    @ActivityMonitoringClass('Create account')
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = OrderedDict(request.data)
            data['free_balance'] = data['debit']
            serializer = self.get_serializer(data=data)
            serializer.fields['free_balance'].read_only = False
            serializer.is_valid(raise_exception=True)
            instance = serializer.save(created_employee=self.request.user)
            return_serializer = AccountLRDSerializer(instance, context={'request': request})
            return Response(return_serializer.data, status=status.HTTP_201_CREATED)
        except APIException as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)

    @ActivityMonitoringClass('Update account')
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            data = OrderedDict(request.data)
            data['free_balance'] = str(round(float(data['debit']) + float(instance.balance), 2))
            serializer = AccountUpdateSecureSerializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            return_serializer = AccountLRDSerializer(instance, context={'request': request})
            return Response(return_serializer.data, status=status.HTTP_200_OK)
        except APIException as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)

    @ActivityMonitoringClass('Delete account')
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response({'message': 'Account has been deleted.'}, status=status.HTTP_200_OK)
        except ProtectedError:
            return Response({'message': 'Deletion impossible. This record has referenced data!'}, status=status.HTTP_400_BAD_REQUEST)
        except APIException as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    @ActivityMonitoringClass('Generate IBAN')
    def generate(self, request, pk=None):
        instance = self.get_object()
        if not instance.number_iban:
            try:
                # Creating IBAN number
                account = str(instance.id_account)
                customer = str(instance.customer_id)
                country_code = ParameterModel.objects.get().country_code
                bank_number = ParameterModel.objects.get().bank_number
                subaccount = AccountTypeModel.objects.get(id_account_type=instance.account_type_id).subaccount
                prefix_zero = ''
                while len(customer) + len(account) + len(prefix_zero) < 12:
                    prefix_zero += '0'
                iban = country_code + bank_number + subaccount + account + prefix_zero + customer
                # Saving IBAN number
                serializer = AccountLRDSerializer(instance, data={'number_iban': iban}, partial=True)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
                return_serializer = AccountLRDSerializer(instance, context={'request': request})
                return Response(return_serializer.data, status=status.HTTP_200_OK)
            except APIException as exc:
                return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'IBAN number already exists.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'])
    @ActivityMonitoringClass('New operation')
    def newoperation(self, request, pk=None):
        instance = self.get_object()
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    serializer_operation = OperationNewSerializer(data=request.data)
                    serializer_operation.is_valid(raise_exception=True)
                    # Choosing operation type
                    if serializer_operation.validated_data['type_operation'] == 2:
                        serializer_operation.validated_data['value_operation'] = serializer_operation.validated_data['value_operation'] * (-1)
                    # Getting data from account
                    balance = AccountModel.objects.get(id_account=instance.id_account).balance
                    debit = AccountModel.objects.get(id_account=instance.id_account).debit
                    # Calculating balance & free_balance after transaction
                    balance_after_operation = balance + serializer_operation.validated_data['value_operation']
                    free_balance_after_operation = balance_after_operation + debit
                    # Updating balance & free balance for account
                    data_account = {
                            'balance': balance_after_operation,
                            'free_balance': free_balance_after_operation}
                    serializer_account = AccountOperationSerializer(instance, data=data_account, partial=True)
                    serializer_account.is_valid(raise_exception=True)
                    instance = serializer_account.save()
                    # Creating new operation
                    serializer_operation.validated_data['id_account'] = instance
                    serializer_operation.validated_data['balance_after_operation'] = balance_after_operation
                    serializer_operation.validated_data['operation_employee'] = self.request.user
                    serializer_operation.save()
            except APIException as exc:
                return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        return_serializer = AccountLRDSerializer(instance, context={'request': request})
        return Response(return_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        instance = self.get_object()
        queryset = OperationModel.objects.filter(id_account=instance.id_account).order_by('-operation_date')
        serializer = OperationHistorySerializer(queryset, context={'request': request}, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    @ActivityMonitoringClass('Interest counting')
    def interest(self, request, pk=None):
        data = AccountModel.objects.filter(balance__gt = 0, percent__gt = 0)
        if data.exists():
            try:
                with transaction.atomic():
                    counter = 0
                    for instance in data:
                        # Calculating data
                        interest = round(instance.balance * (instance.percent / 100),2)
                        new_balance = instance.balance + interest
                        new_free_balance = new_balance + instance.debit
                        # Updating balance & free balance for account
                        data_account = {
                                            "balance": new_balance,
                                            "free_balance": new_free_balance}
                        serializer = AccountOperationSerializer(instance, data=data_account, partial=True)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        # Creating new operation
                        data_operation = {
                                            "type_operation": 3,
                                            "value_operation": interest,
                                            "balance_after_operation": new_balance,
                                            "operation_employee": str(self.request.user),
                                            "id_account": instance.id_account}
                        serializer = OperationInterestSerializer(data=data_operation)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        counter += 1
                    msg = 'Interest for ' + str(counter) + ' account(s) has been recounted.'
                    return Response({'message': msg}, status=status.HTTP_200_OK)
            except APIException as exc:
                return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'No accounts to be recounted.'}, status=status.HTTP_200_OK)


""" Account Type """
class AccountTypeViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = AccountTypeModel.objects.all()
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = AccountTypeFilter
    ordering_fields = ['code']

    def get_serializer_class(self):
        match self.action:
            case 'update':
                return AccountTypeUpdateSerializer
            case _:
                return AccountTypeCLRDSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response({'message': 'Account type has been deleted.'}, status=status.HTTP_200_OK)
        except ProtectedError:
            return Response({'message': 'Deletion impossible. This record has referenced data!'}, status=status.HTTP_400_BAD_REQUEST)


""" Parameter """
class ParameterViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'put']
    queryset = ParameterModel.objects.all()
    serializer_class = ParameterSerializer


""" Log """
class LogViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = LogModel.objects.all().order_by('-date_log')
    serializer_class = LogMonitoringSerializer
