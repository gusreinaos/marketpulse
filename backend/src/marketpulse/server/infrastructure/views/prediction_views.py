# Author: Wojciech Pechmann, Oscar Reina

from ...application.prediction.get_latest_prediction_use_case import GetLatestPredictionUseCase
from ...application.prediction.create_prediction_use_case import CreatePredictionUseCase
from ...application.prediction.create_predictions_use_case import CreatePredictionsUseCase
from ...application.prediction.get_latest_prediction_use_case import GetLatestPredictionUseCase

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

#Import machine learning use cases from the application layer

class PredictionView(viewsets.ViewSet):
    def get_prediction(self, request,*args, **kwargs): 
        cmp = self.kwargs['cmp']
        ts = request.query_params.get('timestamp','')
        
        #timestamp is used to determine if the model shall be trained 
        #is the timestamp NOT blank
        if ts != '':
            if cmp!='':
                try:
                    response = CreatePredictionUseCase.create_new_prediction(cmp)
                    return Response(response, status=status.HTTP_200_OK)
                
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            else:
                return Response({"error": "Invalid action, specify a company"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            if cmp=='':
                try:
                    response = GetLatestPredictionUseCase.get_latest_prediction()
                    return Response(response, status=status.HTTP_200_OK)
                
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                try:                    
                    response = GetLatestPredictionUseCase.get_latest_prediction(cmp)
                    return Response(response, status=status.HTTP_200_OK)
                    
                except Exception as e:
                    print(e)
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_predictions(self, request, *args, **kwargs):
        try:
            response = CreatePredictionsUseCase.create_new_predictions()
            return Response(response, status = status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)