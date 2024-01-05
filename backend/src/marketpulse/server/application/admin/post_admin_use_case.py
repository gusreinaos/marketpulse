# Author: John Berntsson, Oscar Reina


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

class PostAdminUseCase:
    @classmethod
    def create_admin(cls, username, password):
        try:
            #Creates a new default django superuser (admin)
            admin = CustomUser.objects.create_superuser(username=username,
                                            password=password)
            if admin is not None:
                #response = serializers.serialize('json', [user])
                return admin
         
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
