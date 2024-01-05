# Author: John Berntsson

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import logout
from ...application.common.login_use_case import LoginUseCase
from rest_framework import viewsets

class AuthView(viewsets.ViewSet):
    #Login for both customer and admin
    def login_user(self, request, *args, **kwargs):
        try:
            request = LoginUseCase().login_user(request)
            print(request)
            return Response({'username': request.user.username,
                              'id' : request.user.id,
                              'email' : request.user.email,
                              'is_superuser' : request.user.is_superuser,
                              }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    #Logout for both customer and admin
    def logout_user(self, request, *args, **kwargs):
        try:
            logout(request)
            return Response({"message": "Logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)