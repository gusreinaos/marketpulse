# Author: Aditya Khadkikar

from rest_framework import serializers
from server.models import TrainSentimentData

class TrainSentimentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainSentimentData
        fields = '__all__'