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
    def create_customer(cls, username, email, password):
        try:   
            #Creates a new default django user
            user = CustomUser.objects.create_user(
                                            username=username,
                                            password=password,
                                            email=email
                                            )
            response = serializers.serialize('json', [user])
            if user is not None:
                return user
                
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   