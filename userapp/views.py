# -*- coding: utf-8 -*-

from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import APIException
from django.contrib.auth.models import User
from django.http import JsonResponse
from .serializers import RegisterSerializer, ChangePasswordSerializer
from apibankapp.decorators import ActivityMonitoringClass 


class LogoutAPIView(generics.GenericAPIView):
    http_method_names = ["delete"]

    def get_serializer_class(self):
        pass

    def get_serializer(self, *args, **kwargs):
        pass

    @ActivityMonitoringClass(show_data=False)
    def delete(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return JsonResponse(data={"message": "Logout successfully."}, status=status.HTTP_200_OK)


class RegisterAPIView(generics.GenericAPIView):
    http_method_names = ["post"]
    serializer_class = RegisterSerializer

    @ActivityMonitoringClass(show_data=False)
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            account = User(username=serializer.validated_data["username"], email=serializer.validated_data["email"])
            account.set_password(serializer.validated_data["password"])
            account.save()
            data = {}
            data["response"] = "Registration done."
            data["username"] = account.username
            data["email"] = account.email
            token, _ = Token.objects.get_or_create(user=account)
            data["token"] = token.key
            return JsonResponse(data=data, status=status.HTTP_201_CREATED)
        except APIException as exc:
            return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(generics.GenericAPIView):
    http_method_names = ["put"]
    serializer_class = ChangePasswordSerializer

    @ActivityMonitoringClass(show_data=False)
    def put(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = request.user
            if user.check_password(serializer.validated_data["old_password"]):
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                return JsonResponse(data={"message": "Password changed successfully."}, status=status.HTTP_200_OK)
            else:
                return JsonResponse(data={"error": "Incorrect old password."}, status=status.HTTP_400_BAD_REQUEST)
        except APIException as exc:
            return JsonResponse(data=exc.detail, status=status.HTTP_400_BAD_REQUEST)
