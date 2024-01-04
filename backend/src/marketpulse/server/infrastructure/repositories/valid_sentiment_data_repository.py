from ...models import ValidSentimentData

class ValidSentimentDataRepository:
    @classmethod
    def save(cls, data):
        data.save()
        return data

    @classmethod
    def getById(self, r_id):
        try:
            return ValidSentimentData.objects.get(id=r_id)
        except ValidSentimentData.DoesNotExist:
            return None

    @classmethod
    def getByDataPoint(row : str):
        try:
            ValidSentimentData.objects.filter(row=row)
        except ValidSentimentData.DoesNotExist:
            return None
    
    @classmethod
    def getCleanRows(row : str):
        try:
            return ValidSentimentData.objects.values_list('clean', 'sentiment')
        except ValidSentimentData.DoesNotExist:
            return None
    
    @classmethod
    def deleteById(self, r_id):
        try:
            return ValidSentimentData.objects.delete(id=r_id)
        except ValidSentimentData.DoesNotExist:
            return None