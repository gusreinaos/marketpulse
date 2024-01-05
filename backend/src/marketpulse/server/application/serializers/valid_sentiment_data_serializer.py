# Author: Aditya Khadkikar

from rest_framework import serializers
from server.models import ValidSentimentData

class ValidSentimentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidSentimentData
        fields = '__all__'