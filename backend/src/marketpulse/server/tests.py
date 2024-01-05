# Author: Aditya Khadkikar, John Berntsson

from django.test import TestCase
import unittest
from unittest.mock import patch, MagicMock
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN
import datetime, dotenv, sys, os, csv, base64
import seaborn as sns, traceback, glob, logging
from io import StringIO
import matplotlib, numpy as np
from rest_framework import serializers
import pandas as pd
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from .models import TrainSentimentData
from .models import ValidSentimentData
from .infrastructure.repositories.train_sentiment_data_repository import TrainSentimentDataRepository
from .infrastructure.repositories.valid_sentiment_data_repository import ValidSentimentDataRepository
from .application.serializers.train_sentiment_data_serializer import TrainSentimentDataSerializer
from .application.serializers.valid_sentiment_data_serializer import ValidSentimentDataSerializer
from .application.prediction.market_model.train_market_model_use_case import TrainMarketModelUseCase
from .application.prediction.market_model.utils.market_model_data_utils import MarketModelDataUtils
from .application.prediction.sentiment_model.utils.tweet_cleaner_utils import TweetCleanerUtils
from .application.prediction.sentiment_model.utils.sentiment_model_utils import SentimentModelUtils
from .application.prediction.sentiment_model.train_sentiment_model_use_case import TrainSentimentModelUseCase
from .application.prediction.market_model.retrain_market_model_use_case import TrainMarketModelUseCase  # Adjust the import path as necessary
from .application.prediction.market_model.utils.market_model_utils import MarketModelUtils
from .infrastructure.repositories.fred_api_repository import *
from .infrastructure.repositories.company_repository import CompanyRepository
from .infrastructure.repositories.yahoo_api_repository import YahooAPIRepository
from .infrastructure.repositories.tweet_repository import *

# Create your tests here.
class TestSentiment(TestCase):
    mock_df = pd.read_csv("server/application/prediction/sentiment_model/sample_train.csv")
    
    # Test Case 1: Testing whether the data is pre-processed
    def test_tweet_clean(self):
        try:
            self.mock_df.to_csv(os.path.abspath('server/application/prediction/sentiment_model/new_unclean.csv'))
            TweetCleanerUtils.clean_labeled_CSV('new_unclean.csv', 'new_clean.csv', 'text', 'label')
            mock_df_clean = pd.read_csv('new_clean.csv')
            self.assertTrue(os.path.isfile("new_clean.csv"))
            
            ## They should essentially be of the same length (both unprocessed dataset and processed dataset)
            self.assertEqual(len(self.mock_df), len(mock_df_clean))
        except:
            self.fail("Tweet cleaning failed.")

    # Test Case 2: Testing if clean + unclean data is successfully added to DB, and test if data retrieval works from DB
    def test_add_data_to_db(self):
        try:
            self.mock_df.to_csv(os.path.abspath('server/application/prediction/sentiment_model/new_unclean.csv'))
            TweetCleanerUtils.clean_labeled_CSV('new_unclean.csv', 'new_clean.csv', 'text', 'label')
            mock_df_clean = pd.read_csv('new_clean.csv')
            
            mock_df_unclean_train = self.mock_df[['text', 'label']].iloc[:int(0.7*len(self.mock_df))]
            mock_df_unclean_val = self.mock_df[['text', 'label']].iloc[int(0.7*len(self.mock_df)):]
            mock_df_clean_train = mock_df_clean[['text', 'label']].iloc[:int(0.7*len(self.mock_df))]
            mock_df_clean_val = mock_df_clean[['text', 'label']].iloc[int(0.7*len(self.mock_df)):]

            for i in range(len(mock_df_unclean_train)):
                serializer = TrainSentimentDataSerializer(data={
                            'vs_id': '',
                            'unclean': mock_df_unclean_train['text'].iloc[i],
                            'clean': mock_df_clean_train['text'].iloc[i],
                            'sentiment': mock_df_clean_train['label'].iloc[i],
                            'created_at': datetime.datetime.now()
                        })

                try:
                    serializer.is_valid(raise_exception=True)
                except serializers.ValidationError as validation_error:
                    # Handle validation errors and raise them
                    raise validation_error

                # Transform to a class
                new_data = TrainSentimentData(
                    unclean=serializer.validated_data['unclean'],
                    clean=serializer.validated_data['clean'],
                    sentiment=serializer.validated_data['sentiment'],
                    created_at=serializer.validated_data['created_at']
                )

                TrainSentimentDataRepository.save(new_data)

            for i in range(len(mock_df_unclean_val)):
                val_serializer = ValidSentimentDataSerializer(data={
                        'vs_id': '',
                        'unclean': mock_df_unclean_val['text'].iloc[i],
                        'clean': mock_df_clean_val['text'].iloc[i],
                        'sentiment': mock_df_clean_val['label'].iloc[i],
                        'created_at': datetime.datetime.now()
                    })

                try:
                    val_serializer.is_valid(raise_exception=True)
                except serializers.ValidationError as validation_error:
                    # Handle validation errors and raise them
                    raise validation_error

                # Transform to a class
                val_new_data = ValidSentimentData(
                    unclean=val_serializer.validated_data['unclean'],
                    clean=val_serializer.validated_data['clean'],
                    sentiment=val_serializer.validated_data['sentiment'],
                    created_at=val_serializer.validated_data['created_at']
                )

                val_saved_data = ValidSentimentDataRepository.save(val_new_data)

            self.assertGreater(len(list(TrainSentimentDataRepository.getCleanRows())), 0)
            self.assertGreater(len(list(ValidSentimentDataRepository.getCleanRows())), 0)
        except:
            logging.error(traceback.format_exc())
            self.fail("Adding, and retrieving data from DB failed.")
    
    # Test Case 3: Test if train() method works successfully on correctly structured data, as per schema
    def test_data_match_model_schema(self):
        # Load dataset with the right schema
        try:
            with open("server/application/prediction/sentiment_model/sample_train.csv") as f:
                stringified = f.read() + '\n'
            TrainSentimentModelUseCase.train('07-2023-12-18', bytes(stringified, 'utf-8').decode('utf-8'))
        except:
            logging.error(traceback.format_exc)
            self.fail("Training for dataset with right schema failed.")

    # Test Case 4: Test if train() method correctly handles the error when data is not abiding by the schema, and aborts training
    def test_data_detect_improper_data(self):
        # Load dataset which does not follow the schema that is required (in a file called sample_train_ws (ws ==> wrongly structured))
        with open("server/application/prediction/sentiment_model/sample_train_ws.csv") as f:
            wrong_stringified = f.read() + '\n'
        self.assertFalse(TrainSentimentModelUseCase.train('07-2023-12-18', bytes(wrong_stringified, 'utf-8').decode('utf-8')), "Training for dataset with wrong schema was supposed to fail.")

    # Test Case 5: Test that the model returns an output value between 0, 1 and 2
    def test_model_return(self):
        mock_df_clean = pd.read_csv('new_clean.csv')

        # Set a mock variable as the loaded model
        mock_model = SentimentModelUtils.get_model('07-2023-12-18')
        
        # Get the predictions array by running the model with the data
        mock_predictions = SentimentModelUtils.run_model(mock_model, mock_df_clean['text'])

        for num in mock_predictions:
            if num not in [0,1,2]:
                self.fail("Model is not returning an output in the right value ranges (must be either 0,1,2).")
                
class TestMarketTrend(TestCase):
    # Testing whether data is retrieved using the getInflationRate(), getGDP and/or similar
    def test_get_data_from_source(self):
        GDP_data = getGDPData('2015-01-01', '2020-12-31')
        inflation_data = getInflationData('2015-01-01', '2020-12-01')
        
        assert GDP_data.shape == (24,)
        assert inflation_data.shape == (72,)
        #print("shape",GDP_data.shape)
        #print(GDP_data)
        #print("Inflation data:", inflation_data)


    # Checking whether initial data is converted correctly to normalized values (-1:1) and binary mapping
    def test_data_clean(self):
        """Normalization doesn't work if theres not data from different dates I think
        max_val and min_val is the same so it tries to divide by 0, like if theres only tweets from one GDP date"""
        x_train, y_train, x_val, y_val = MarketModelDataUtils.collect_data(cmp="AAPL", data_file_path="server/application/prediction/market_model/trend_data/input_data.csv")
        
        for train_example in x_train:
            for col in train_example:
                for num in col:
                    if (num < -1) or (num > 1):
                        self.fail("Not Normalized.")

        for train_example in x_val:
            for col in train_example:
                for num in col:
                    if (num < -1) or (num > 1):
                        self.fail("Not Normalized.")

    # Testing whether model returns the right output based on prediction
    def test_model_return(self):
        mock_sentiment_averages = [2,2,1,2,0,1,2,0,0,0,0,0,0,0,1,2,2,2,2,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2]
        received_pred, received_close = MarketModelUtils.analyze_trend(mock_sentiment_averages, "AAPL")
        print(received_pred)
        if received_pred not in [0,1,2]:
            self.fail("Model is not returning a value as per the limits; must be a market trend prediction output between 0 and 2.")