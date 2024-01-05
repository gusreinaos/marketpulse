# Author: Aditya Khadkikar

from ...models import TrainSentimentData
import datetime

class TrainSentimentDataRepository:
    @classmethod
    def save(cls, data):
        data.save()
        return data

    @classmethod
    def getById(self, r_id):
        try:
            return TrainSentimentData.objects.get(id=r_id)
        except TrainSentimentData.DoesNotExist:
            return None

    @classmethod
    def getCleanRows(row : str):
        try:
            return TrainSentimentData.objects.values_list('clean', 'sentiment')
        except TrainSentimentData.DoesNotExist:
            return None

    @classmethod
    def getCurrentRows(row : str):
        try:
            return TrainSentimentData.objects.filter(created_at__gte=(datetime.datetime.today()-datetime.timedelta(days=2)), created_at__lte=datetime.datetime.now()).values_list('clean', 'sentiment')
        except TrainSentimentData.DoesNotExist:
            return None

    @classmethod
    def deleteById(self, r_id):
        try:
            return TrainSentimentData.objects.delete(id=r_id)
        except TrainSentimentData.DoesNotExist:
            return None