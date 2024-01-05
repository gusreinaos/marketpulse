# Author: Burak Askan, Oscar Reina

from django.db import IntegrityError
import tensorflow as tf
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from ...application.prediction.market_model.retrain_market_model_use_case import TrainMarketModelUseCase
from ...application.prediction.market_model.utils.market_model_utils import MarketModelUtils

import glob, os, json

class MarketModelView(viewsets.ViewSet):
    def get_market_model_versions(self, request, *args, **kwargs):
        try:
            print("TRENDMODELVIEW")
            versions = glob.glob('server/application/prediction/market_model/trained/**')
            response = json.dumps({"model_vers": [os.path.basename(file) for file in versions]})
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)

    def get_market_production_model(self, request, *args, **kwargs):
        try:
            response = MarketModelUtils.get_trend_production_model()
            return Response({'response': response}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)

    def get_market_model_information(self, request, *args, **kwargs):
        print("TRENDINFOVIEW")
        if ('model_version' in self.kwargs):
            version = self.kwargs['model_version']

            ## May need to be removed later, but we need some way to show the accuracy of the current model
            response = MarketModelUtils.trend_accuracy(version)
            response = {'model': version, 'summary': (response.get('summary')), 
                'history': {
                    'accuracy': '%.3f'%(response.get('accuracy')),
                    'loss': '%.3f'%(response.get('loss'))
                },
                'heatmap': response.get('heatmap')
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

    
    def post_market_model_version(self, request, *args, **kwargs):
        try:
            print("TRENDTRAINVIEW")
            version = self.kwargs['model_version']
            training_file = request.FILES.get('csv-to-train').read().decode('utf-8')
            response = TrainMarketModelUseCase.retrain_model(version, training_file)

            return Response({'response': response}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
    def update_market_model_version(self, request, *args, **kwargs):
        try:
            version = self.kwargs['model_version']
            response = MarketModelUtils.set_trend_model(version)
            return Response({'response': response}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
