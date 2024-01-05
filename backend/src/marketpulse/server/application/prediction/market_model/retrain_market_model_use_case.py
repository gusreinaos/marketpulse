# Author: Burak Askan, Michael Larsson

from keras.models import Sequential
from keras.utils import to_categorical
from keras.layers import Dense, SimpleRNN
import numpy as np
from datetime import datetime
import traceback, glob, os
from io import StringIO
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from ....infrastructure.repositories.fred_api_repository import *
from ....infrastructure.repositories.yahoo_api_repository import YahooAPIRepository
from ....infrastructure.repositories.company_repository import CompanyRepository
from ....infrastructure.repositories.tweet_repository import *
from .utils.market_model_utils import MarketModelUtils
from .utils.market_model_data_utils import MarketModelDataUtils

class TrainMarketModelUseCase:

    @classmethod
    def retrain_model(self, version, training_file):

        
        response = True

            
        companies = CompanyRepository.get_trainable_companies()

        new_csv_path = 'server/application/prediction/market_model/trend_data/inputted_data.csv'

        raw_csv = StringIO(training_file)
        df = pd.read_csv(raw_csv).replace({-1:0})

        df.to_csv(os.path.join(new_csv_path))

        model = MarketModelUtils.load_model(version)

        x_train = []
        y_train = []
        x_val =  []
        y_val =  []
        for cmp in companies:
            cmp = cmp.company_code
            x_train_cmp, y_train_cmp, x_val_cmp, y_val_cmp = MarketModelDataUtils.collect_data(cmp, new_csv_path)
    
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
        new_vers = f'{int(max(versions)[0])+1}-{today_date.strftime("%Y-%m-%d")}'

        model.save(f'server/application/prediction/market_model/trained/{new_vers}', save_format='tf')

        response = new_vers
        return response 