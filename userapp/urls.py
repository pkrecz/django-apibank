# -*- coding: utf-8 -*-

from django.urls import path
from .views import LoginAPIView, LogoutAPIView, RegisterAPIView, ChangePasswordAPIView


urlpatterns = [
    path(route="login/", view=LoginAPIView.as_view(), name="login"),
    path(route="logout/", view=LogoutAPIView.as_view(), name="logout"),
    path(route="register/", view=RegisterAPIView.as_view(), name="register"),
    path(route="change-password/", view=ChangePasswordAPIView.as_view(), name="change-password"),
]
