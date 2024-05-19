from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(style={'input': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True}}
    
    def save(self):
        password = self.validated_data['password']
        password_confirm = self.validated_data['password_confirm']
        email = self.validated_data['email']
        if password != password_confirm:
            raise serializers.ValidationError({'error': 'Passwords should be the same!'})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'E-mail already exists!'})
        account = User(username=self.validated_data['username'], email=email)
        account.set_password(password)
        account.save()
        return account
    