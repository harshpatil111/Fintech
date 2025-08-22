from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        data = self.get_serializer(data=request.data)
        data.is_valid(raise_exception=True)
        return Response(data.validated_data)

class SocialLoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        return Response({'detail':'Social login not yet implemented'})

class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        # Stub — integrate email sending later
        return Response({'detail':'Password reset email sent (mock).'})


