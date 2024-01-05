# Author: Burak Askan

from ...models import TrainTrendData
import pandas as pd

class TrainTrendDataRepository:
    @classmethod
    def save(cls, data):
        data.save()
        return data

    @classmethod
    def getById(self, r_id):
        try:
            return TrainTrendData.objects.get(id=r_id)
        except TrainTrendData.DoesNotExist:
            return None
        
    @classmethod
    def getByCmp(self, r_cmp):
        try:
            predictions = TrainTrendData.objects.filter(ticker_symbol=r_cmp)
            predictions_data = [{'ticker_symbol': prediction.ticker_symbol, 'post_date': prediction.post_date, 'sentiment': prediction.sentiment} for prediction in predictions]

            return predictions_data
        except TrainTrendData.DoesNotExist:
            return None

    @classmethod
    def bulkCreate(self, model_instances):
        try:
            TrainTrendData.objects.bulk_create(model_instances)
        except TrainTrendData.DoesNotExist:
            return None

    @classmethod
    def deleteById(self, r_id):
        try:
            return TrainTrendData.objects.delete(id=r_id)
        except TrainTrendData.DoesNotExist:
            return None