# -*- coding: utf-8 -*-

import os
import logging
from django.urls import reverse
from django.contrib.auth.models import User


def sub_test_register(client, input_data):
	url = reverse("register")
	response = client.post(url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Register testing ...")
	assert response.status_code == 201
	assert response_json["username"] == "fake_user"
	assert response_json["token"] is not None
	logging.info("Register testing finished.")


def sub_test_login(client, input_data):
	url = reverse("login")
	response = client.post(url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Login testing ...")
	assert response.status_code == 200
	assert response_json["token"] is not None
	logging.info("Login testing finished.")
	os.environ["USER_NAME"] = input_data["username"]


def sub_test_change_password(client, input_data):
	url = reverse("change-password")
	user = User.objects.filter(username=os.environ["USER_NAME"]).first()
	client.force_authenticate(user=user)
	response = client.put(url, data=input_data, format="json")
	response_json = response.json()
	logging.info("Changing password testing ...")
	assert response.status_code == 200
	assert response_json == {"message": "Password changed successfully."}
	logging.info("Changing password testing finished.")


def sub_test_logout(client):
	url = reverse("logout")
	user = User.objects.filter(username=os.environ["USER_NAME"]).first()
	client.force_authenticate(user=user)
	response = client.delete(url)
	response_json = response.json()
	logging.info("Logout testing ...")
	assert response.status_code == 200
	assert response_json == {"message": "Logout successfully."}
	logging.info("Logout testing finished.")


# Test to be performed.
def test_auth(
                client_test,
                data_test_register,
                data_test_login,
                data_test_change_password):

    logging.info("START - authentication testing")
    sub_test_register(client_test, data_test_register)
    sub_test_login(client_test, data_test_login)
    sub_test_change_password(client_test, data_test_change_password)
    sub_test_logout(client_test)
    logging.info("STOP - authentication testing")
