from keras.models import Sequential
from keras.layers import Dense, SimpleRNN
import tensorflow as tf
import numpy as np
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
from .....infrastructure.repositories.fred_api_repository import *
from .....infrastructure.repositories.yahoo_api_repository import YahooAPIRepository
from .....infrastructure.repositories.tweet_repository import *

class MarketModelDataUtils:

    @classmethod
    def merge_features(self, company_tweet, close_price, inflation, gdp):
        close_gdp_data = pd.merge(close_price, gdp, left_index=True, right_index=True, how='inner')
        close_gdp_inflation_data = pd.merge(close_gdp_data, inflation, left_index=True, right_index=True, how='inner')
        close_gdp_inflation_sentiment_data = pd.merge(close_gdp_inflation_data, company_tweet, left_index=True, right_index=True, how='inner')
        close_gdp_inflation_sentiment_data.rename(columns={"value_x": "GDP"}, inplace=True)
        close_gdp_inflation_sentiment_data.rename(columns={"value_y": "Inflation Rate"}, inplace=True)
        return close_gdp_inflation_sentiment_data

    @classmethod
    def normalize_data(self, data):
        if(type(data) != float):
            data = pd.to_numeric(data, errors='coerce')

        min_val = min(data)
        max_val = max(data)
        normalized_data = [2 * ((val - min_val) / (max_val - min_val)) - 1 for val in data]
        return normalized_data

    @classmethod
    def map_to_binary(self, value, threshold=0.5):
        if value < -threshold:
            return -1
        elif -threshold <= value <= threshold:
            return 0
        else:
            return 1
        
    @classmethod
    def temp_merge(self, close_price, gdp, inflation):
        gdp.rename("GDP", inplace=True)
        inflation.rename("InflationRate", inplace=True)
        close_gdp_data = pd.merge(close_price,gdp, left_index=True, right_index=True, how='inner')
        close_gdp_inflation_data = pd.merge(close_gdp_data, inflation, left_index=True, right_index=True, how='inner')
        return close_gdp_inflation_data

    @classmethod
    def collect_data(self, cmp, data_file_path): 
        start_yf = datetime(2014,12, 31)
        end_yf = datetime(2020, 12, 31)

        start_fred = '2015-01-01'
        end_fred = '2020-12-31'

        gdp_data = getGDPData(start_fred, end_fred)
        # Resample the data to fill in missing dates
        gdp_data = gdp_data.resample('D').mean()
        # Interpolate the missing values
        gdp_data = gdp_data.interpolate()

        inf_data = getInflationData(start_fred, end_fred)
        # Resample the data to fill in missing dates
        inf_data = inf_data.resample('D').mean()
        # Interpolate the missing values
        inf_data = inf_data.interpolate()

        tweets_data = get_tweet_sentiments(cmp, data_file_path)
        close_data = YahooAPIRepository.get_finance_date(start_yf, end_yf, cmp)

        all_info = MarketModelDataUtils.merge_features(tweets_data, close_data, inf_data, gdp_data)
        
        cols_to_nor = ['Close', 'GDP', 'Inflation Rate', 'sentiment']
        normalized_data = all_info[cols_to_nor].apply(MarketModelDataUtils.normalize_data)

        data = normalized_data.values

        training_data_len = int(np.ceil(len(data) * .80))

        train_data = data[0:int(training_data_len), :]

        x_train = []
        y_train = []

        for i in range(60, len(train_data)):
            x_train.append(train_data[i-60:i,])
            y_train.append(train_data[i, 0])
        
        x_train, y_train = np.array(x_train), np.array(y_train)

        for i in range(0, len(y_train)):
            y_train[i] = MarketModelDataUtils.map_to_binary(y_train[i])

        val_data_len = int(np.ceil(len(data))) - training_data_len

        val_data = data[val_data_len: , :]

        x_val = []
        y_val = []

        for i in range(60, len(train_data)):
            x_val.append(val_data[i-60:i,])
            y_val.append(MarketModelDataUtils.map_to_binary(val_data[i, 0]))

        x_val, y_val = np.array(x_val), np.array(y_val)

        return x_train, y_train, x_val, y_val