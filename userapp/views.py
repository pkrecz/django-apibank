from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import (RegisterSerializer, ChangePasswordSerializer)


class LogoutAPIView(generics.GenericAPIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class RegisterAPIView(generics.GenericAPIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = User(username=serializer.validated_data['username'], email=serializer.validated_data['email'])
        account.set_password(serializer.validated_data['password'])
        account.save()
        data = {}
        data['response'] = 'Registration done.'
        data['username'] = account.username
        data['email'] = account.email
        token, _ = Token.objects.get_or_create(user=account)
        data['token'] = token.key
        return Response(data=data, status=status.HTTP_201_CREATED)


class ChangePasswordAPIView(generics.GenericAPIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if user.check_password(serializer.validated_data['old_password']):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': ['Password changed successfully.']}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ['Incorrect old password.']}, status=status.HTTP_400_BAD_REQUEST)
