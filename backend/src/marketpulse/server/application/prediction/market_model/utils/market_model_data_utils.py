# Author: Michael Larsson, Burak Askan

from keras.models import Sequential
from keras.layers import Dense, SimpleRNN
import tensorflow as tf
import numpy as np
from datetime import datetime
import matplotlib
import traceback
matplotlib.use('Agg')
from .....infrastructure.repositories.fred_api_repository import *
from .....infrastructure.repositories.yahoo_api_repository import YahooAPIRepository
from .....infrastructure.repositories.tweet_repository import *

class MarketModelDataUtils:

    @classmethod
    def merge_features(self, company_tweet, close_price, inflation, gdp):
        print()
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
    def map_to_binary(self, value, threshold=0.25):
        if value < -threshold:
            return 0
        elif -threshold <= value <= threshold:
            return 1
        else:
            return 2
        
    @classmethod
    def temp_merge(self, close_price, gdp, inflation):
        gdp.rename("GDP", inplace=True)
        inflation.rename("InflationRate", inplace=True)
        close_gdp_data = pd.merge(close_price,gdp, left_index=True, right_index=True, how='inner')
        close_gdp_inflation_data = pd.merge(close_gdp_data, inflation, left_index=True, right_index=True, how='inner')
        return close_gdp_inflation_data

    @classmethod
    def collect_data(self, cmp, data_file_path): 
        try:
            tweets_data, start_date, end_date = get_tweet_sentiments(cmp, data_file_path)
            start_date_fred = start_date.strftime('%Y-%m-%d')
            end_date_fred = end_date.strftime('%Y-%m-%d')
           
            gdp_data = getGDPData(start_date_fred, end_date_fred)
            print(gdp_data)
            # Resample the data to fill in missing dates
            gdp_data = gdp_data.resample('D').mean()
            # Interpolate the missing values
            gdp_data = gdp_data.interpolate()

            inf_data = getInflationData(start_date_fred, end_date_fred)
            # Resample the data to fill in missing dates
            inf_data = inf_data.resample('D').mean()
            # Interpolate the missing values
            inf_data = inf_data.interpolate()

            close_data = YahooAPIRepository.get_finance_date(start_date, end_date, cmp)

            all_info = MarketModelDataUtils.merge_features(tweets_data, close_data, inf_data, gdp_data)
            
            cols_to_nor = ['Close', 'GDP', 'Inflation Rate', 'sentiment']
            normalized_data = all_info[cols_to_nor].apply(MarketModelDataUtils.normalize_data)

            data = normalized_data.values

            #train_data = data[0:int(training_data_len), :]

            data_batchs_x = []
            data_batchs_y = []
            for i in range(60, len(data)):
                data_batchs_x.append(data[i-60:i,])
                data_batchs_y.append(data[i, 0])
            
            data_batchs_x, data_batchs_y = np.array(data_batchs_x), np.array(data_batchs_y)

            permuted_index = np.random.permutation(len(data_batchs_x))

            data_batchs_x = data_batchs_x[permuted_index]
            data_batchs_y = data_batchs_y[permuted_index]

            
            x_train = []
            y_train = []

            training_data_len = int(np.ceil(len(data_batchs_x) * .80))

            for i in range(0, training_data_len):
                x_train.append(data_batchs_x[i])
                y_train.append(MarketModelDataUtils.map_to_binary(data_batchs_y[i]))

            x_val = []
            y_val = []
            for i in range(training_data_len, len(data_batchs_x)):
                x_val.append(data_batchs_x[i])
                y_val.append(MarketModelDataUtils.map_to_binary(data_batchs_y[i]))
            
            
            x_train, y_train = np.array(x_train), np.array(y_train)

            x_val, y_val = np.array(x_val), np.array(y_val)

            return x_train, y_train, x_val, y_val
        
        except Exception  as e:
            print("Running into issues")
            traceback.print_exc()
            return e