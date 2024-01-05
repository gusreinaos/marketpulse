# Author: Wojciech Pechmann

from rest_framework import serializers
from server.models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyListSerializer(serializers.ListSerializer):
    child = CompanySerializer()