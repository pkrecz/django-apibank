from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(style={'input': 'password'}, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True}}

    def save(self):
        password = self.validated_data['password']
        account = User(username=self.validated_data['username'], email=self.validated_data['email'])
        account.set_password(password)
        account.save()
        return account

    def validate_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'error': 'Passwords should be the same!'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'E-mail already exists!'})
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input': 'password'}, write_only=True, required=True)
    new_password = serializers.CharField(style={'input': 'password'}, write_only=True, required=True)
    new_password_confirm = serializers.CharField(style={'input': 'password'}, write_only=True, required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({'error': 'Passwords should be the same!'})      
        return data
