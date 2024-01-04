from keras.models import Sequential
from keras.layers import Dense, SimpleRNN
import numpy as np
from datetime import datetime
import dotenv
import sys, os, csv, base64, seaborn as sns
import traceback, glob
from io import StringIO
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from .utils.market_model_data_utils import MarketModelDataUtils
from ....infrastructure.repositories.fred_api_repository import *
from ....infrastructure.repositories.company_repository import CompanyRepository
from ....infrastructure.repositories.yahoo_api_repository import YahooAPIRepository
from ....infrastructure.repositories.tweet_repository import *

COMPANIES = ["AAPL", "GOOG", "MSFT", "TSLA", "AMZN", "GOOGL"]

class TrainMarketModelUseCase:

    @classmethod
    def trainModel(self):

        model = Sequential()
        model.add(SimpleRNN(units=124, input_shape=(None, 4)))
        model.add(Dense(units=1, activation='tanh'))  # Output layer with tanh activation for -1, 0, 1 result

        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

        for cmp in COMPANIES:
            x_train, y_train, x_val, y_val = MarketModelDataUtils.collect_data(cmp, "")
            model_log = model.fit(x_train, y_train, epochs=1,validation_data=(x_val, y_val) , batch_size=1)
        
        today_date = datetime.now()
        ver_names = glob.glob('server/application/prediction/market_model/trained/**')
        versions = [os.path.basename(file) for file in ver_names]

        
        print("This is the log: ")
        print(model_log.history)

        model.save(f'server/application/prediction/market_model/trained/{int(max(versions)[0])+1}-{today_date.strftime("%Y-%m-%d")}', save_format='tf')