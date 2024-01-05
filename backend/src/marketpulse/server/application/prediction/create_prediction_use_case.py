# Author: Burak Askan, Wojciech Pechmann

from ..serializers.prediction_serializer import *
import datetime 
from ...infrastructure.repositories.prediction_repository import PredictionRepository
from ..serializers.prediction_serializer import PredictionSerializer
from .market_model.utils.market_model_utils import MarketModelUtils
from .sentiment_model.utils.sentiment_model_utils import SentimentModelUtils
from ...models import Prediction 
from rest_framework import serializers
from ...infrastructure.repositories.stocktwit_api_repository import StocktwitApiRepository
import dotenv
import os

class CreatePredictionUseCase:
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    SENTIMENT_MODEL_VERSION = os.environ["SENTIMENT_MODEL_VER"]
    TREND_MODEL_VERSION = os.environ["MARKET_MODEL_VER"]


    @classmethod
    def tweet_rate(self, twits):
        twit_arr = []
        print(twits)
        for twit in twits:
            twit_arr.append(datetime.datetime.fromisoformat(twit.get('created_at').rstrip("Z")))

        latest_date = max(twit_arr)
        oldest_date = min(twit_arr)

        time_diff = latest_date - oldest_date
        num_tweets = len(twit_arr)

        tweet_rate = num_tweets/time_diff.total_seconds()
       
        return tweet_rate



    @classmethod
    def create_new_prediction(self, company:str):      

        twits = StocktwitApiRepository.get_stocktwits_for_company(company)

        twit_arr = [twit.get('body') for twit in twits]
    
       
        tweet_rate_val = self.tweet_rate(twits)
        
        sentiment_list = SentimentModelUtils.analyze_tweets(twit_arr, CreatePredictionUseCase.SENTIMENT_MODEL_VERSION)
        
        avg_sentiment = sum(sentiment_list)/len(sentiment_list)

        pred_val, stock_val = MarketModelUtils.analyze_trend(sentiment_list, company)

        serializer = PredictionSerializer(data={
            'prediction_id': '',
            'prediction_value': pred_val,
            'created_at': datetime.datetime.now(),
            'company_code': company,
            'avg_sentiment': avg_sentiment,
            'tweet_rate': tweet_rate_val,
            'stock_val': stock_val,
        })

        try:
            serializer.is_valid(raise_exception=True)

        except serializers.ValidationError as validation_error:
            raise validation_error
        
        new_prediction = Prediction(
            prediction_value=serializer.validated_data['prediction_value'],
            created_at=serializer.validated_data['created_at'],
            company_code=serializer.validated_data['company_code'],
            avg_sentiment=serializer.validated_data['avg_sentiment'],
            tweet_rate=serializer.validated_data['tweet_rate'],
            stock_val=serializer.validated_data['stock_val']
        )

        PredictionRepository.save(new_prediction)

        response = serializer.data

        return response