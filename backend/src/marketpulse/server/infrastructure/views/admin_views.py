# Author: John Berntsson

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...application.admin.post_admin_use_case import PostAdminUseCase
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from ...models import CustomUser
from django.contrib.auth.models import User, UserManager
from django.core import serializers
from django.shortcuts import redirect, render

class AdminView(viewsets.ViewSet):
    def post(self, request, *args, **kwargs):
        try:
            password = request.data.get('password')
            username = request.data.get('username')
            PostAdminUseCase.create_admin(username=username, password=password)      
            return Response({"message": "Admin created"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
#Create an initial superuser 
    #post(username='admin', password='admin')
