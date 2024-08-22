# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.parsers import (MultiPartParser, FormParser, JSONParser)
from django.http import JsonResponse
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
from .filters import (CustomerFilter, AccountFilter, AccountTypeFilter, OperationFilter, LogFilter)


""" Customer """
class CustomerViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    queryset = CustomerModel.objects.all()
    filterset_class = CustomerFilter
    search_fields = ['pesel', 'identification']
    ordering_fields = ['last_name', 'first_name']
    ordering = ['last_name']

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
            return JsonResponse(data={'message': 'Customer has been deleted.'}, status=status.HTTP_200_OK)
        except ProtectedError:
            return JsonResponse(data={'message': 'Deletion impossible. This record has referenced data!'}, status=status.HTTP_400_BAD_REQUEST)
        except APIException as exc:
            return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save(created_employee=self.request.user)
            return_serializer = CustomerLRDSerializer(instance, context={'request': request})
            return JsonResponse(data=return_serializer.data, status=status.HTTP_201_CREATED)
        except APIException as exc:
            return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)


""" Account """
class AccountViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = AccountModel.objects.all()
    filterset_class = AccountFilter
    search_fields = ['number_iban']
    ordering_fields = ['number_iban']

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

    @ActivityMonitoringClass()
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
            return JsonResponse(data=return_serializer.data, status=status.HTTP_201_CREATED)
        except APIException as exc:
            return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)

    @ActivityMonitoringClass()
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
            return JsonResponse(data=return_serializer.data, status=status.HTTP_200_OK)
        except APIException as exc:
            return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)

    @ActivityMonitoringClass()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return JsonResponse(data={'message': 'Account has been deleted.'}, status=status.HTTP_200_OK)
        except ProtectedError:
            return JsonResponse(data={'message': 'Deletion impossible. This record has referenced data!'}, status=status.HTTP_400_BAD_REQUEST)
        except APIException as exc:
            return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    @ActivityMonitoringClass()
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
                return JsonResponse(data=return_serializer.data, status=status.HTTP_200_OK)
            except APIException as exc:
                return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'message': 'IBAN number already exists.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'])
    @ActivityMonitoringClass()
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
                    serializer_operation.save(operation_employee=self.request.user)
            except APIException as exc:
                return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)
        return_serializer = AccountLRDSerializer(instance, context={'request': request})
        return JsonResponse(data=return_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    @ActivityMonitoringClass()
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
                                            "id_account": instance.id_account}
                        serializer = OperationInterestSerializer(data=data_operation)
                        serializer.is_valid(raise_exception=True)
                        serializer.save(operation_employee=self.request.user)
                        counter += 1
                    msg = 'Interest for ' + str(counter) + ' account(s) has been recounted.'
                    return JsonResponse(data={'message': msg}, status=status.HTTP_200_OK)
            except APIException as exc:
                return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(data={'message': 'No accounts to be recounted.'}, status=status.HTTP_200_OK)


""" Account Type """
class AccountTypeViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = AccountTypeModel.objects.all()
    filterset_class = AccountTypeFilter
    search_fields = ['code', 'description']
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
            return JsonResponse(data={'message': 'Account type has been deleted.'}, status=status.HTTP_200_OK)
        except ProtectedError:
            return JsonResponse(data={'message': 'Deletion impossible. This record has referenced data!'}, status=status.HTTP_400_BAD_REQUEST)


""" Operation """
class OperationViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = OperationModel.objects.all()
    filterset_class = OperationFilter
    search_fields = ['type_operation']
    ordering_fields = ['operation_date']
    ordering = ['-operation_date']

    def retrieve(self, request, *args, **kwargs):
        try:
            queryset = OperationModel.objects.filter(id_account=self.kwargs['pk']).order_by('-operation_date')
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = OperationHistorySerializer(page, context={'request': request}, many=True)
                return self.get_paginated_response(data=serializer.data)
            serializer = OperationHistorySerializer(queryset, context={'request': request}, many=True)
            return JsonResponse(data=serializer.data, safe=False, status=status.HTTP_200_OK)
        except APIException as exc:
                return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)


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
    filterset_class = LogFilter
    search_fields = ['user_log']
    ordering_fields = ['date_log', 'duration_log']
    ordering = ['-duration_log']
