# Author: Wojciech Pechmann

from ...models import Prediction
from django.db.models.aggregates import Max
from rest_framework import serializers
from django.db.models import OuterRef, Subquery
import pandas as pd

class PredictionRepository:
    @classmethod
    def save(cls, prediction):
        prediction.save()
        return prediction

    @classmethod
    def get_by_id(self, p_id):
        try:
            return Prediction.objects.get(id=p_id)
        except Prediction.DoesNotExist:
            return None
        
    @classmethod
    def get_all_predictions(self):
        try:
            return Prediction.objects.all()
        except Prediction.DoesNotExist:
            return None



    @classmethod
    def get_by_company(self, code : str):
        try:
            Prediction.objects.filter(company_code=code)
        except Prediction.DoesNotExist:
            return None

    @classmethod
    def get_latest(self):
        try:
            latest_created_at = Prediction.objects.filter(
                company_code=OuterRef('company_code')
            ).order_by('-created_at').values('created_at')[:1]

            latest_predictions = Prediction.objects.filter(
                created_at=Subquery(latest_created_at)
            ).values('company_code', 'prediction_value', 'tweet_rate', 'avg_sentiment', 'stock_val', 'created_at')

            latest_predictions_list = list(latest_predictions)

            merged_df = pd.DataFrame.from_records(latest_predictions_list)

            return merged_df
        except Prediction.DoesNotExist:
            return None
    
    @classmethod
    def get_latest_by_company(self, code: str):
        try:
            latest_data = Prediction.objects.filter(company_code=code).latest('created_at')
            return latest_data
            
        except Prediction.DoesNotExist:
            return None
            
    
    @classmethod
    def delete_by_id(self, p_id):
        try:
            return Prediction.objects.delete(id=p_id)
        except Prediction.DoesNotExist:
            return None
    

