from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...application.customer.post_customer_use_case import PostCustomerUseCase
from ...application.customer.get_favorites_use_case import GetFavoritesUseCase
from ...application.customer.post_favorite_use_case import PostFavoriteUseCase
from ...application.customer.delete_favorite_use_case import DeleteFavoriteUseCase
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from ...models import CustomUser
from django.contrib.auth.models import User, UserManager
from django.core import serializers
from django.shortcuts import redirect, render

class CustomerView(viewsets.ViewSet):
    def post(self, request, *args, **kwargs):
        try:
            password = request.data.get('password')
            email = request.data.get('email')
            username = request.data.get('username')
            user = PostCustomerUseCase.create_customer(username=username, email=email, password=password)
            print(user.id)
            response = serializers.serialize('json', [user])
            #print(response)
            return Response({"message": "Customer created"}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get_favorites(self, request, *args, **kwargs):
        #try:            
            cid = self.kwargs['cid']

            response = GetFavoritesUseCase.get(cid)
            return Response(response, status=status.HTTP_200_OK)
        
        #except Exception as e:
            print(f'Unexpected error occured: {e}')
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post_favorite(self, request, *args, **kwargs):
        #try:
            cid = self.kwargs['cid']
            cmp = self.kwargs['cmp']

            response = PostFavoriteUseCase.post(cid,cmp)
            return Response(response, status=status.HTTP_200_OK)


        #except Exception as e:
            print(f'Unexpected error occured: {e}')
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_favorite(self, request, *args, **kwargs):
        #try:
            cid = self.kwargs['cid']
            cmp = self.kwargs['cmp']

            response = DeleteFavoriteUseCase.delete(cid,cmp)
            return Response(response, status=status.HTTP_200_OK)

        #except Exception as e:
            print(f'Unexpected error occured: {e}')
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)