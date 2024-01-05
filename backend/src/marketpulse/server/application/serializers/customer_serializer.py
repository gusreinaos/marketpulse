# Author: John Berntsson

from rest_framework import serializers
from ...models import CustomUser

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','username', 'email', 'password','is_superuser')
        extra_kwargs = {'password': {'write_only': True}}
