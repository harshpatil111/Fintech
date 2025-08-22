from rest_framework.views import APIView
from rest_framework.response import Response

class RegisterView(APIView):
    def post(self, request):
        # Replace with your registration logic
        return Response({"message": "User registered successfully"})

class LoginView(APIView):
    def post(self, request):
        # Replace with your login logic
        return Response({"message": "User logged in successfully"})