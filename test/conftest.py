# -*- coding: utf-8 -*-

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


# Preparing envoirment for testing
@pytest.fixture
def db_no_rollback(request, django_db_setup, django_db_blocker):
    django_db_blocker.unblock()
    request.addfinalizer(django_db_blocker.restore)

@pytest.fixture
def db_access_without_rollback_and_truncate(request, django_db_setup, django_db_blocker):
    django_db_blocker.unblock()
    yield
    django_db_blocker.restore()

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db): 
    pass

@pytest.fixture
def client_test():
    user = User.objects.create_superuser(username='test_user', password='test_password')
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client


# Preparing sample data
@pytest.fixture
def data_test_create_customer():
    return {
            "first_name": "John",
            "last_name": "Walker",
            "street": "GreenWood",
            "house": "1",
            "apartment": "3A",
            "postal_code": "45-200",
            "city": "Los Angeles",
            "pesel": "89071203452",
            "birth_date": "1989-07-12",
            "birth_city": "New York",
            "identification": "ABX9234"}

@pytest.fixture
def data_test_update_customer():
    return {
            "first_name": "Arnold",
            "last_name": "Hunter",
            "street": "GreenWood",
            "house": "12",
            "apartment": "",
            "postal_code": "45-200",
            "city": "Los Angeles",
            "pesel": "89071203452",
            "birth_date": "1989-07-12",
            "birth_city": "New York",
            "identification": "ABX9234"}

@pytest.fixture
def data_test_create_accounttype():
    return {
            "code": "S-01",
            "description": "Standard account",
            "subaccount": "994500",
            "percent": 7.35}

@pytest.fixture
def data_test_update_accounttype():
    return {
            "description": "Standard account",
            "subaccount": "037540",
            "percent": 7.55}

@pytest.fixture
def data_test_create_parameter():
    return {
            "country_code": "PL",
            "bank_number": "10101397"}

@pytest.fixture
def data_test_create_account():
    return {
            "debit": 1000,
            "percent": 1.25}

@pytest.fixture
def data_test_update_account():
    return {
            "debit": 50,
            "percent": 1.85}

@pytest.fixture
def data_test_deposit_account():
    return {
        "type_operation": 1,
        "value_operation": 100}

@pytest.fixture
def data_test_withdrawal_account():
    return {
        "type_operation": 2,
        "value_operation": 50}


# Preparing dat for authentication test
@pytest.fixture
def data_test_register():
    return {
        "username": "fake_user",
        "email": "fake_user@example.com",
        "password": "pass100@test",
        "password_confirm": "pass100@test"}

@pytest.fixture
def data_test_login():
    return {
        "username": "fake_user",
        "password": "pass100@test"}

@pytest.fixture
def data_test_change_password():
    return {
        "old_password": "pass100@test",
        "new_password": "pass100@new",
        "new_password_confirm": "pass100@new"}
