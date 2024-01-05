# Author: John Berntsson, Oscar Reina

from django.db import IntegrityError
from ..serializers.customer_serializer import CustomerSerializer
from ...infrastructure.repositories.customer_repository import CustomerRepository
from ...models import CustomUser
import uuid
from django.contrib.auth.models import User, UserManager
from django.core import serializers
from django.shortcuts import redirect, render
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import status

class LoginUserUseCase:
    def login_user(self, request, *args, **kwargs):
       
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
            response = serializers.serialize('json', [request])
    
            if user is not None:
                #If user was found,we log in the user (creates a django_session object in the database)
                #session object has the user id, we can also add other attributes to the session object if we want
                login(request, user)
                
                return Response({'message': 'Logged in'}, status=status.HTTP_200_OK)
            else:
                 return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
                 
        except Exception as e:
                return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            