# Author: Aditya Khadkikar, Oscar Reina

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from ...application.prediction.sentiment_model.train_sentiment_model_use_case import TrainSentimentModelUseCase
from ...application.prediction.sentiment_model.utils.sentiment_model_utils import SentimentModelUtils

import glob, os, json

class SentimentModelView(viewsets.ViewSet):
    def get_sentiment_model_versions(self, request, *args, **kwargs):
        try:
            versions = glob.glob('server/application/prediction/sentiment_model/versions/**')
            print(versions)
            response = json.dumps({"model_vers": [os.path.basename(file) for file in versions]})
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_sentiment_production_model(self, request, *args, **kwargs):
        response = SentimentModelUtils.get_production_model()
        return Response({'response': response}, status=status.HTTP_200_OK)
    
    def get_sentiment_model_information(self, request, *args, **kwargs):
        if ('model_version' in self.kwargs):
            version = self.kwargs['model_version']
            response = SentimentModelUtils.get_accuracy(version)
            response = {'model': version, 'summary': (response.get('summary')), 
                'history': {
                    'accuracy': '%.3f'%(response.get('accuracy')),
                    'loss': '%.3f'%(response.get('loss'))
                },
                'heatmap': (response.get('heatmap'))
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post_sentiment_model_version(self, request, *args, **kwargs):
        try:
            version = self.kwargs['model_version']
            training_file = request.FILES.get('csv-to-train').read().decode('utf-8')
            response = TrainSentimentModelUseCase.train(version, training_file)
            return Response({'response': response}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
    def update_sentiment_model_version(self, request, *args, **kwargs):
        try:
            print("SENTIMENTSETVIEW")
            version = self.kwargs['model_version']
            response = SentimentModelUtils.set_sentiment_model(version)
            return Response({'response': response}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
