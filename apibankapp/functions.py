# -*- coding: utf-8 -*-

import json
from .serializers import LogMonitoringSerializer
from .models import AccountModel


class RegisterErrorClass:

    def register_error(self, request):
        user_log = str(request.user)
        data_log = json.dumps(request.data)
        action = self.action
        function = self.__class__.__name__
        status_log = "Failed"
        data = {
                "action_log": action,
                "function_log": function,
                "duration_log": 0,
                "data_log": data_log[:250],
                "user_log": user_log,
                "status_log": status_log}
        serializer = LogMonitoringSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


def generate_iban(country_code, bank_number, subaccount, account, customer):
    prefix_zero = ""
    while len(customer) + len(account) + len(prefix_zero) < 12:
        prefix_zero += "0"
    iban = country_code + bank_number + subaccount + account + prefix_zero + customer
    return str(iban)


def get_balance_and_debit(id_account):
    balance = AccountModel.objects.get(id_account=id_account).balance
    debit = AccountModel.objects.get(id_account=id_account).debit
    return balance, debit
