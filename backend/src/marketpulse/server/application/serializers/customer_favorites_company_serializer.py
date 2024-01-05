# Author: Wojciech Pechmann

from rest_framework import serializers
from ...models import UserFavoritesCompany

class CustomerFavoritesCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoritesCompany
        fields = '__all__'
