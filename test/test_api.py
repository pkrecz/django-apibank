# -*- coding: utf-8 -*-

import os
import logging
from django.urls import reverse
from django.conf import settings

list_of_files_to_be_deleted = []


def sub_test_create_customer(client, input_data):
	url = reverse("customers-list")
	response = client.post(path=url, data=input_data, format="multipart")
	response_json = response.json()
	logging.info("Creation customer testing ...")
	assert response.status_code == 201
	assert response_json["first_name"] == "John"
	assert response_json["last_name"] == "Walker"
	assert response_json["street"] == "GreenWood"
	assert response_json["house"] == "1"
	assert response_json["apartment"] == "3A"
	assert response_json["postal_code"] == "45-200"
	assert response_json["city"] == "Los Angeles"
	assert response_json["pesel"] == "89071203452"
	assert response_json["birth_date"] == "1989-07-12"
	assert response_json["birth_city"] == "New York"
	assert response_json["identification"] == "ABX9234"
	assert response_json["avatar"] is not None
	assert response_json["created_date"] is not None
	assert response_json["created_employee"] is not None
	logging.info("Creation customer testing finished.")
	os.environ["CUSTOMER_ID"] = str(response_json["id_customer"])
	list_of_files_to_be_deleted.append(response_json["avatar"])


def sub_test_update_customer(client, input_data):
	id_customer = os.environ["CUSTOMER_ID"]
	url = reverse("customers-detail", kwargs={"pk": int(id_customer)})
	response = client.put(path=url, data=input_data, format="multipart")
	response_json = response.json()
	logging.info("Update customer testing ...")
	assert response.status_code == 200
	assert response_json["first_name"] == "Arnold"
	assert response_json["last_name"] == "Hunter"
	assert response_json["street"] == "GreenWood"
	assert response_json["house"] == "12"
	assert response_json["apartment"] == ""
	assert response_json["postal_code"] == "45-200"
	assert response_json["city"] == "Los Angeles"
	assert response_json["pesel"] == "89071203452"
	assert response_json["birth_date"] == "1989-07-12"
	assert response_json["birth_city"] == "New York"
	assert response_json["identification"] == "ABX9234"
	assert response_json["avatar"] is not None
	logging.info("Update customer testing finished.")
	list_of_files_to_be_deleted.append(response_json["avatar"])


def sub_test_get_customer(client):
	id_customer = os.environ["CUSTOMER_ID"]
	url = reverse("customers-detail", kwargs={"pk": int(id_customer)})
	response = client.get(path=url)
	response_json = response.json()
	logging.info("Get customer testing ...")
	assert response.status_code == 200
	assert response_json["first_name"] == "Arnold"
	assert response_json["last_name"] == "Hunter"
	logging.info("Get customer testing finished.")


def sub_test_delete_customer(client):
	id_customer = os.environ["CUSTOMER_ID"]
	url = reverse("customers-detail", kwargs={"pk": int(id_customer)})
	response = client.delete(path=url)
	response_json = response.json()
	logging.info("Delete customer testing ...")
	assert response.status_code == 200
	assert response_json == {"message": "Customer has been deleted."}
	logging.info("Delete customer testing finished.")


def sub_test_create_accounttype(client, input_data):
	url = reverse("accounttypes-list")
	response = client.post(path=url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Creation account type testing ...")
	assert response.status_code == 201
	assert response_json["code"] == "S-01"
	assert response_json["description"] == "Standard account"
	assert response_json["subaccount"] == "994500"
	assert response_json["percent"] == "7.35"
	logging.info("Creation account type testing finished.")
	os.environ["ACCOUNT_TYPE_ID"] = str(response_json["id_account_type"])


def sub_test_update_accounttype(client, input_data):
	id_account_type = os.environ["ACCOUNT_TYPE_ID"]
	url = reverse("accounttypes-detail", kwargs={"pk": int(id_account_type)})
	response = client.put(path=url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Update account type testing ...")
	assert response.status_code == 200
	assert response_json["description"] == "Standard account"
	assert response_json["subaccount"] == "037540"
	assert response_json["percent"] == "7.55"
	logging.info("Update account type testing finished.")


def sub_test_get_accounttype(client):
	id_account_type = os.environ["ACCOUNT_TYPE_ID"]
	url = reverse("accounttypes-detail", kwargs={"pk": int(id_account_type)})
	response = client.get(path=url)
	response_json = response.json()
	logging.info("Get account type testing ...")
	assert response.status_code == 200
	assert response_json["description"] == "Standard account"
	assert response_json["subaccount"] == "037540"
	assert response_json["percent"] == "7.55"
	logging.info("Get account type testing finished.")


def sub_test_delete_accounttype(client):
	id_account_type = os.environ["ACCOUNT_TYPE_ID"]
	url = reverse("accounttypes-detail", kwargs={"pk": int(id_account_type)})
	response = client.delete(path=url)
	response_json = response.json()
	logging.info("Delete account type testing ...")
	assert response.status_code == 200
	assert response_json == {"message": "Account type has been deleted."}
	logging.info("Delete account type testing finished.")


def sub_test_create_parameter(client, input_data):
	url = reverse("parameters-list")
	response = client.post(path=url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Creation parameter testing ...")
	assert response.status_code == 201
	assert response_json["country_code"] == "PL"
	assert response_json["bank_number"] == "10101397"
	logging.info("Creation parameter testing finished.")


def sub_test_create_account(client, input_data):
	id_customer = os.environ["CUSTOMER_ID"]
	id_account_type = os.environ["ACCOUNT_TYPE_ID"]
	input_data.update({"customer": id_customer, "account_type": id_account_type})
	url = reverse("accounts-list")
	response = client.post(path=url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Creation account testing ...")
	assert response.status_code == 201
	assert response_json["debit"] == "1000.00"
	assert response_json["percent"] == "1.25"
	assert response_json["free_balance"] == "1000.00"
	assert response_json["created_date"] is not None
	assert response_json["created_employee"] is not None
	logging.info("Creation account testing finished.")
	os.environ["ACCOUNT_ID"] = str(response_json["id_account"])


def sub_test_update_account(client, input_data):
	id_account = os.environ["ACCOUNT_ID"]
	url = reverse("accounts-detail", kwargs={"pk": int(id_account)})
	response = client.put(path=url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Update account testing ...")
	assert response.status_code == 200
	assert response_json["debit"] == "50.00"
	assert response_json["percent"] == "1.85"
	assert float(response_json["free_balance"]) == float(response_json["balance"]) + float(response_json["debit"])
	logging.info("Update account testing finished.")


def sub_test_generate_iban_account(client):
	id_account = os.environ["ACCOUNT_ID"]
	url = reverse("accounts-detail", kwargs={"pk": int(id_account)})
	response = client.get(path=url + "generate/")
	response_json = response.json()
	logging.info("Generating IBAN testing ...")
	assert response.status_code == 200
	assert len(response_json["number_iban"]) == 28
	logging.info("Generating IBAN testing finished.")


def sub_test_deposit_account(client, input_data):
	id_account = os.environ["ACCOUNT_ID"]
	url = reverse("accounts-detail", kwargs={"pk": int(id_account)})
	response = client.post(path=url + "newoperation/", data=input_data, format="json")
	response_json = response.json()
	logging.info("Deposit testing ...")
	assert response.status_code == 200
	assert response_json["free_balance"] == "1100.00"
	assert float(response_json["free_balance"]) == float(response_json["balance"]) + float(response_json["debit"])
	logging.info("Deposit testing finished.")


def sub_test_get_deposit_operation(client):
	id_account = os.environ["ACCOUNT_ID"]
	url = reverse("accounts-detail", kwargs={"pk": int(id_account)})
	response = client.get(path=url + "operations/")
	response_json = response.json()["results"][0]
	logging.info("Deposit operation testing ...")
	assert response.status_code == 200
	assert response_json["type_operation"] == "Deposit"
	assert response_json["value_operation"] == "100.00"
	assert response_json["balance_after_operation"] == "100.00"
	assert response_json["operation_date"] is not None
	assert response_json["operation_employee"] is not None
	logging.info("Deposit operation testing finished.")


def sub_test_withdrawal_account(client, input_data):
	id_account = os.environ["ACCOUNT_ID"]
	url = reverse("accounts-detail", kwargs={"pk": int(id_account)})
	response = client.post(path=url + "newoperation/", data=input_data, format="json")
	response_json = response.json()
	logging.info("Withdrawal testing ...")
	assert response.status_code == 200
	assert response_json["free_balance"] == "950.00"
	assert float(response_json["free_balance"]) == float(response_json["balance"]) + float(response_json["debit"])
	logging.info("Withdrawal testing finished.")


def sub_test_get_withdrawal_operation(client):
	id_account = os.environ["ACCOUNT_ID"]
	url = reverse("accounts-detail", kwargs={"pk": int(id_account)})
	response = client.get(path=url + "operations/")
	response_json = response.json()["results"][0]
	logging.info("Withdrawal operation testing ...")
	assert response.status_code == 200
	assert response_json["type_operation"] == "Withdrawal"
	assert response_json["value_operation"] == "-50.00"
	assert response_json["balance_after_operation"] == "-50.00"
	assert response_json["operation_date"] is not None
	assert response_json["operation_employee"] is not None
	logging.info("Withdrawal operation testing finished.")


def sub_test_interest_counting(client, result):
	url = reverse("accounts-list")
	response = client.get(path=url + "interest/")
	response_json = response.json()
	logging.info("Interest operation testing ...")
	assert response.status_code == 200
	assert response_json == result
	logging.info("Interest operation testing finished.")


def sub_test_deletion_media_files(list_of_files):
	logging.info("Deletion files operation testing ...")
	for file in list_of_files:
			file_name = os.path.basename(file)
			file_path = os.path.join(settings.MEDIA_ROOT, "image", "avatars", file_name)
			assert os.path.exists(file_path) == True
			if os.path.exists(file_path):
					os.remove(file_path)
	logging.info("Deletion files operation testing finished.")


# Test to be performed.
def test_model(
					client_test,
					data_test_create_customer,
					data_test_update_customer,
					data_test_create_accounttype,
					data_test_update_accounttype,
					data_test_create_parameter):
	logging.info("START - model testing")
	sub_test_create_customer(client_test, data_test_create_customer)
	sub_test_update_customer(client_test, data_test_update_customer)
	sub_test_get_customer(client_test)
	sub_test_delete_customer(client_test)
	sub_test_create_accounttype(client_test, data_test_create_accounttype)
	sub_test_update_accounttype(client_test, data_test_update_accounttype)
	sub_test_get_accounttype(client_test)
	sub_test_delete_accounttype(client_test)
	sub_test_create_parameter(client_test, data_test_create_parameter)
	logging.info("STOP - model testing")


def test_flow_basic(
					client_test,
					data_test_create_parameter,
					data_test_create_customer,
					data_test_create_accounttype,
					data_test_create_account,
					data_test_update_account):
	logging.info("START - standard flow")
	sub_test_create_parameter(client_test, data_test_create_parameter)
	sub_test_create_customer(client_test, data_test_create_customer)
	sub_test_create_accounttype(client_test, data_test_create_accounttype)
	sub_test_create_account(client_test, data_test_create_account)
	sub_test_update_account(client_test, data_test_update_account)
	sub_test_generate_iban_account(client_test)
	logging.info("STOP - standard flow")


def test_scenario_deposit(
					client_test,
					data_test_create_parameter,
					data_test_create_customer,
					data_test_create_accounttype,
					data_test_create_account,
					data_test_deposit_account):
	logging.info("START - scenario deposit")
	sub_test_create_parameter(client_test, data_test_create_parameter)
	sub_test_create_customer(client_test, data_test_create_customer)
	sub_test_create_accounttype(client_test, data_test_create_accounttype)
	sub_test_create_account(client_test, data_test_create_account)
	sub_test_deposit_account(client_test, data_test_deposit_account)
	sub_test_get_deposit_operation(client_test)
	logging.info("STOP - scenario deposit")


def test_scenario_withdrawal(
					client_test,
					data_test_create_parameter,
					data_test_create_customer,
					data_test_create_accounttype,
					data_test_create_account,
					data_test_withdrawal_account):
	logging.info("START - scenario withdrawal")
	sub_test_create_parameter(client_test, data_test_create_parameter)
	sub_test_create_customer(client_test, data_test_create_customer)
	sub_test_create_accounttype(client_test, data_test_create_accounttype)
	sub_test_create_account(client_test, data_test_create_account)
	sub_test_withdrawal_account(client_test, data_test_withdrawal_account)
	sub_test_get_withdrawal_operation(client_test)
	logging.info("STOP - scenario withdrawal")


def test_scenario_interest_counting(
					client_test,
					data_test_create_parameter,
					data_test_create_customer,
					data_test_create_accounttype,
					data_test_create_account,
					data_test_deposit_account):
	logging.info("START - scenario interest")
	sub_test_create_parameter(client_test, data_test_create_parameter)
	sub_test_create_customer(client_test, data_test_create_customer)
	sub_test_create_accounttype(client_test, data_test_create_accounttype)
	sub_test_create_account(client_test, data_test_create_account)
	sub_test_interest_counting(client_test, {"message": "No accounts to be recounted."})
	sub_test_deposit_account(client_test, data_test_deposit_account)
	sub_test_interest_counting(client_test, {"message": "Interest for 1 account(s) has been recounted."})
	logging.info("START - scenario interest")


def test_other_operation():
	logging.info("START - other operation")
	sub_test_deletion_media_files(list_of_files_to_be_deleted)
	logging.info("STOP - other operation")
