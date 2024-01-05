# Author: John Berntsson

from django.db import IntegrityError
from ..serializers.customer_serializer import CustomerSerializer
from ...infrastructure.repositories.customer_repository import CustomerRepository
from ...models import CustomUser
from rest_framework import serializers
import uuid
from django.contrib.auth.models import User, UserManager
from django.core import serializers
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework import status

def generate_uuid():
    return str(uuid.uuid4())

class PostCustomerUseCase:
    @classmethod
    def create_customer(self, **request_data):
        try:
            username = request_data.get('username')
            email = request_data.get('email')
            password = request_data.get('password')
            serializer = CustomerSerializer(data={'username': username, 'email': email, 'password': password})
            
            # Validate the serializer
            if serializer.is_valid():
                user = CustomUser.objects.create_user(
                username=serializer.validated_data.get('username'),
                    email=serializer.validated_data.get('email'),
                    password=serializer.validated_data.get('password')
                )
                return user
            else:
            # Return validation errors
                raise ValueError(serializer.errors)
        except Exception as e:
            print(e)
        