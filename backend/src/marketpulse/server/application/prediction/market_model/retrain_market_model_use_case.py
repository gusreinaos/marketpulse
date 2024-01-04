from keras.models import Sequential
from keras.layers import Dense, SimpleRNN
import numpy as np
from datetime import datetime
import traceback, glob, os
from io import StringIO
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from http import response
from ....infrastructure.repositories.fred_api_repository import *
from ....infrastructure.repositories.yahoo_api_repository import YahooAPIRepository
from ....infrastructure.repositories.company_repository import CompanyRepository
from ....infrastructure.repositories.tweet_repository import *
from .utils.market_model_utils import MarketModelUtils
from .utils.market_model_data_utils import MarketModelDataUtils

class TrainMarketModelUseCase:

    @classmethod
    def retrain_model(version, training_file):
        response = True
        try:

            companies = CompanyRepository.get_trainable_companies()

            new_csv_path = 'server/application/prediction/market_model/trend_data/inputted_data.csv'

            raw_csv = StringIO(training_file)
            df = pd.read_csv(raw_csv).replace({-1:0})

            df.to_csv(os.path.join(new_csv_path))

            model = MarketModelUtils.load_model(version)
            
            for cmp in companies:
                x_train, y_train, x_val, y_val = MarketModelDataUtils.collect_data(cmp, new_csv_path)
                print("RNN Results:")
                model_log = model.fit(x_train, y_train, epochs=1,validation_data=(x_val, y_val) , batch_size=1)
                print("This is the summary: ")
                print(model.summary())
            
            today_date = datetime.now()
            ver_names = glob.glob('server/application/prediction/market_model/trained/**')
            versions = [os.path.basename(file) for file in ver_names]

            new_vers = f'{int(max(versions)[0])+1}-{today_date.strftime("%Y-%m-%d")}'
            model.save(f'server/application/prediction/market_model/trained/{new_vers}', save_format='tf') 

            response = new_vers

            return response 
        
        except Exception as error:
            print(error)
            response = False
            return response