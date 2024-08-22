# -*- coding: utf-8 -*-

from django_filters.rest_framework import (FilterSet, CharFilter, DateFilter, NumberFilter)


class CustomerFilter(FilterSet):
    last_name = CharFilter(field_name='last_name', lookup_expr='icontains')


class AccountFilter(FilterSet):
    number_iban = CharFilter(field_name='number_iban', lookup_expr='icontains')


class AccountTypeFilter(FilterSet):
    code = CharFilter(field_name='code', lookup_expr='istartswith')


class OperationFilter(FilterSet):
    type_operation = NumberFilter(field_name='type_operation')
    value_operation = NumberFilter(field_name='value_operation')
    operation_date = DateFilter(field_name='operation_date', lookup_expr='date__iexact')


class LogFilter(FilterSet):
    date_log = DateFilter(field_name='date_log', lookup_expr='date__iexact')
    user_log = CharFilter(field_name='user_log', lookup_expr='icontains')
    status_log = CharFilter(field_name='status_log', lookup_expr='istartswith')
