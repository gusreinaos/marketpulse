# Author: Wojciech Pechmann

from rest_framework import serializers
from server.models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'