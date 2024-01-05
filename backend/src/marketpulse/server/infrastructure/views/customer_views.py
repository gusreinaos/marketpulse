# Author: John Berntsson

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from ...application.customer.post_customer_use_case import PostCustomerUseCase
from ...application.customer.get_favorites_use_case import GetFavoritesUseCase
from ...application.customer.post_favorite_use_case import PostFavoriteUseCase
from ...application.customer.delete_favorite_use_case import DeleteFavoriteUseCase
from rest_framework import viewsets
from ...models import CustomUser
from ...application.serializers.customer_serializer import CustomerSerializer
from django.contrib.auth.hashers import make_password

class CustomerView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomerSerializer

    def partial_update(self, request, *args, **kwargs):
        """
        Update a customer's information, only the fields that are provided in the request will be updated.
        Empty string values or whitespaces-only values will be ignored.
        Returns the fields specified in the serializer.
        To change which fields can be updated, update the CustomerSerializer.
        """
        instance = self.get_object()

        # Clean the request data by removing fields with empty or whitespace-only values
        cleaned_data = {key: value.strip() for key, value in request.data.items() if key != 'password'}
        
        # Handle password field specifically, if present in the request
        if 'password' in request.data and request.data['password'].strip():
            cleaned_data['password'] = request.data['password'].strip()

        serializer = self.get_serializer(instance, data=cleaned_data, partial=True)

        if serializer.is_valid():
            # Additional logic as required, e.g., handling password field
            if 'password' in serializer.validated_data:
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def create(self, request, *args, **kwargs):
        try:
            user = PostCustomerUseCase().create_customer(**request.data)
            return Response({"message": "Customer created"}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"errors": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
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