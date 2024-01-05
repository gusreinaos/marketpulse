# Author: Burak Askan, Wojciech Pechmann

from ...models import Prediction 
from ...infrastructure.repositories.stocktwit_api_repository import StocktwitApiRepository
from ...infrastructure.repositories.company_repository import CompanyRepository
from ...infrastructure.repositories.prediction_repository import PredictionRepository
from ..serializers.prediction_serializer import PredictionSerializer
from .sentiment_model.utils.sentiment_model_utils import SentimentModelUtils
from .market_model.utils.market_model_utils import MarketModelUtils
from ..serializers.prediction_serializer import *

import dotenv
import os
import time
import datetime 
from rest_framework import serializers

class CreatePredictionsUseCase:
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    SENTIMENT_MODEL_VERSION = os.environ["SENTIMENT_MODEL_VER"]
    #TREND_MODEL_VERSION = os.environ["MARKET_MODEL_VER"]

    @classmethod
    def create_new_predictions(cls):
        
        companies = CompanyRepository.get_all()
        responses = []

        for company_instance in companies:
            twits = StocktwitApiRepository.get_stocktwits_for_company(company_instance.company_code)
            twit_arr = [twit.get('body') for twit in twits]

            sentiment_list = SentimentModelUtils.analyze_tweets(twit_arr, cls.SENTIMENT_MODEL_VERSION)
            pred_val = MarketModelUtils.analyze_trend(sentiment_list, company_instance)

            serializer = PredictionSerializer(data={
                'prediction_id': '',
                'prediction_value': pred_val,
                'created_at': datetime.datetime.now(),
                'company_code': company_instance,
            })

            try:
                serializer.is_valid(raise_exception=True)

            except serializers.ValidationError as validation_error:
                raise validation_error

            new_prediction = Prediction(
                prediction_value=serializer.validated_data['prediction_value'],
                created_at=serializer.validated_data['created_at'],
                company_code=serializer.validated_data['company_code'],
            )

            PredictionRepository.save(new_prediction)
            responses.append(serializer.data)

            print(serializer.data)

            time.sleep(5)

        return responses