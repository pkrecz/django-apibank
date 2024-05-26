from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import RegisterSerializer, ChangePasswordSerializer


@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def register_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        data['response'] = 'Registration done.'
        data['username'] = account.username
        data['email'] = account.email
        token, _ = Token.objects.get_or_create(user=account)
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if user.check_password(serializer.validated_data['old_password']):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
