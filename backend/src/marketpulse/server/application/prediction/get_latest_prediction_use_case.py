# Author: Wojciech Pechmann, Burak Askan

from ..serializers.prediction_serializer import *
import datetime 
from ...infrastructure.repositories.prediction_repository import PredictionRepository
from ..serializers.prediction_serializer import PredictionSerializer
from .market_model.utils.market_model_utils import MarketModelUtils
from .sentiment_model.utils.sentiment_model_utils import SentimentModelUtils
from ...models import Prediction 
from rest_framework import serializers
from ...infrastructure.repositories.stocktwit_api_repository import StocktwitApiRepository
from .create_prediction_use_case import CreatePredictionUseCase

class GetLatestPredictionUseCase:
    """
        Generates a new prediction and saves it to the database.

        Args:
            CharField: Input data containing company stock code.

        Returns:
            A prediction object data including:
            Float: The prediction of market trend
            DateTime: The date&time when this prediction was made
            CharField: A string containing the company stock code

        Raises:
            serializers.ValidationError: If input data is not valid.
            IntegrityError: If there is an integrity violation during saving.
    """
    @classmethod
    def get_latest_prediction(cls, company):
        unserialized_data = PredictionRepository.get_latest_by_company(company)

        if not unserialized_data or ((datetime.datetime.now().replace(tzinfo=None) - unserialized_data.created_at.replace(tzinfo=None)).days > 1):
            response = CreatePredictionUseCase.create_new_prediction(company)

        else:
            serializer = PredictionSerializer(unserialized_data)
            response = serializer.data

        return response