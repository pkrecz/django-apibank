# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={"input": "password"}, write_only=True, required=True)
    password_confirm = serializers.CharField(style={"input": "password"}, write_only=True, required=True)

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(detail={"message": "Passwords should be the same!"}, code=400)
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(detail={"message": "E-mail already exists!"}, code=400)
        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError(detail={"message": "Username already exists!"}, code=400)
        return data

    def validate_password(self, value):
        validate_password(value)
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={"input": "password"}, write_only=True, required=True)
    new_password = serializers.CharField(style={"input": "password"}, write_only=True, required=True)
    new_password_confirm = serializers.CharField(style={"input": "password"}, write_only=True, required=True)

    def validate(self, data):
        if data["new_password"] != data["new_password_confirm"]:
            raise serializers.ValidationError(detail={"message": "Passwords should be the same!"}, code=400)
        if data["old_password"] == data["new_password"]:
            raise serializers.ValidationError(detail={"message": "Old and new passwords can not be the same!"}, code=400)
        return data

    def validate_new_password(self, value):
        validate_password(value)
        return value
