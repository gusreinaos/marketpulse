# Author: John Berntsson, Oscar Reina


from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework import status

class LoginUseCase:
    def login_user(self, request, *args, **kwargs):
      
        try:
            username = request.data.get('username')
            password = request.data.get('password')
           
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                print(request.user.is_authenticated)
                print(request.session.get('_auth_user_id'))
                print('sesssion data',request.session.__dict__)
                return request

            else:
                 return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                print(f"Unexpected error: {e}")
                raise Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            