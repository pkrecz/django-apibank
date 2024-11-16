# -*- coding: utf-8 -*-

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import LogoutAPIView, RegisterAPIView, ChangePasswordAPIView


urlpatterns = [
    path(route="login/", view=obtain_auth_token, name="login"),
    path(route="logout/", view=LogoutAPIView.as_view(), name="logout"),
    path(route="register/", view=RegisterAPIView.as_view(), name="register"),
    path(route="change-password/", view=ChangePasswordAPIView.as_view(), name="change-password"),
]
