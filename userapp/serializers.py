from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(style={'input': 'password'}, write_only=True, required=True)
    password_confirm = serializers.CharField(style={'input': 'password'}, write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'error': 'Passwords should be the same!'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'E-mail already exists!'})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'error': 'Username already exists!'})
        return data

    def validate_password(self, value):
        validate_password(value)
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input': 'password'}, write_only=True, required=True)
    new_password = serializers.CharField(style={'input': 'password'}, write_only=True, required=True)
    new_password_confirm = serializers.CharField(style={'input': 'password'}, write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({'error': 'Passwords should be the same!'})
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({'error': 'Old and new passwords can not be the same!'})    
        return data
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
