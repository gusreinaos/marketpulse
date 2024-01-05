# Author: Burak Askan, Michael Larsson

from keras.models import Sequential
from keras.utils import to_categorical
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
    def trainModel(cls):
        model = Sequential()
        model.add(SimpleRNN(units=124, input_shape=(None, 4)))  # Adjust input_shape based on your actual input dimensions
        model.add(Dense(units=3, activation='softmax'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        x_train = []
        y_train = []
        x_val =  []
        y_val =  []
        lens = []

        for cmp in COMPANIES:
            x_train_cmp, y_train_cmp, x_val_cmp, y_val_cmp = MarketModelDataUtils.collect_data(cmp, "")
            lens.append(len(x_train_cmp))
            print(cmp)
            print(len(x_train_cmp))
            print(len(x_val_cmp))
            x_train.extend(x_train_cmp)  # Use concatenate
            y_train.extend(y_train_cmp)  # Use concatenate
            x_val.extend(x_val_cmp)  # Use concatenate
            y_val.extend(y_val_cmp)  # Use concatenate

        x_train.extend(x_train)
        y_train.extend(y_train)
        x_train = np.array(x_train)
        y_train = np.array(y_train)
        x_val = np.array(x_val)
        y_val = np.array(y_val)

        y_train_categorical = to_categorical(y_train, num_classes=3)
        y_val_categorical = to_categorical(y_val, num_classes=3)
        model_log = model.fit(x_train, y_train_categorical, epochs=1, validation_data=(x_val, y_val_categorical), batch_size=1)
        
        today_date = datetime.now()
        ver_names = glob.glob('server/application/prediction/market_model/trained/**')
        versions = [os.path.basename(file) for file in ver_names]

        print("This is the log:")
        print(model_log.history)

        model.save(f'server/application/prediction/market_model/trained/1', save_format='tf')
