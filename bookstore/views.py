from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)


class UserPasswordResetAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            # Código para enviar o email de redefinição de senha entra aqui
            return Response({'detail': 'Email de redefinição de senha enviado'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)