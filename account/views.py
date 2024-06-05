from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,PasswordResetRequestSerializer,PasswordResetConfirmSerializer
from account.renderers import UserRenderer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.models import User,PasswordResetToken
from django.utils.crypto import get_random_string
from account.utils import send_email
from django.shortcuts import render
from .permissions import IsAdminUser
from rest_framework import generics, permissions


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Success'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileUpdateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self, request, format=None):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'msg': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        token = get_random_string(length=64)
        PasswordResetToken.objects.create(user=user, token=token)

        domain_with_port = request.get_host()


        reset_link = f"http://{domain_with_port}/api/user/reset-password/?token={token}/"

        email_data = {
            'subject':'Password Reset Request',
            'body':f'Click the link to reset your password: {reset_link}',
            'to_email':email
        }
        send_email(email_data)

        return Response({'msg': 'Password reset link sent'}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    def get(self, request, format=None):
        token = request.GET.get('token')
        if not token:
            return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        return render(request, 'password_change.html', {'token': token})
    
    def post(self, request, format=None):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'msg': 'Password has been reset successfully'}, status=status.HTTP_200_OK)


def user_list(request):
    if request.user.is_authenticated and request.user.is_staff:
        users = User.objects.all()
        return render(request, 'admin_customize/user_list.html', {'users': users})
    else:
        return render(request, 'unauthorized.html')
