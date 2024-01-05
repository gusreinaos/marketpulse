# Author: Micahel Larsson, Burak Askan

#File for the purpose of running the market trend model 
import pandas as pd
from keras.utils import to_categorical
import numpy as np
import os, base64, seaborn as sns
import tensorflow as tf
from matplotlib import pyplot as plt
import os
import datetime
import dateutil.relativedelta as relativedelta
from sklearn.metrics import confusion_matrix, classification_report
import dotenv
from lime import lime_tabular
from .market_model_data_utils import MarketModelDataUtils
from .....infrastructure.repositories.prediction_repository import PredictionRepository
from .....infrastructure.repositories.yahoo_api_repository import YahooAPIRepository
from .....infrastructure.repositories.fred_api_repository import *

class MarketModelUtils:
    
    @classmethod
    def load_model(self, model_ver: int):
        model_dir = os.path.abspath(f'./server/application/prediction/market_model/trained/{model_ver}')
        #load model
        model = tf.keras.models.load_model(model_dir, compile=False)

        return model    
    
    @classmethod
    def load_model(self, model_ver: int):
        model_dir = os.path.abspath(f'./server/application/prediction/market_model/trained/{model_ver}')
        #load model
        model = tf.keras.models.load_model(model_dir)
        return model 
    
    @classmethod
    def get_trend_production_model(self):
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)

        TREND_MODEL_VERSION =  os.environ["MARKET_MODEL_VER"]
        return TREND_MODEL_VERSION
    
    @classmethod
    def analyze_trend(self, sentiment_dataset: list, cmp):

        TREND_MODEL_VERSION = self.get_trend_production_model()

        DATA_GAP = 60
        
        model = MarketModelUtils.load_model(TREND_MODEL_VERSION)

        today_date = datetime.datetime.now().strftime('%Y-%m-%d')

        start_date = (datetime.datetime.now() - relativedelta.relativedelta(months=DATA_GAP)).strftime('%Y-%m-%d')

        stock_val = YahooAPIRepository.get_finance_date(start_date, today_date, cmp)

        gdp_val = getGDPData(start_date, today_date)

        inf_val = getInflationData(start_date, today_date)

        avg_sentiment = sum(sentiment_dataset)/len(sentiment_dataset)

        x_new_data = MarketModelDataUtils.temp_merge(stock_val, gdp_val, inf_val)

        latest_close = x_new_data.iloc[-1]['Close']

        cols_to_nor = ['Close', 'GDP', 'InflationRate']

        x_new_data_norm = x_new_data[cols_to_nor].apply(MarketModelDataUtils.normalize_data)

        stock_val = x_new_data_norm.iloc[-1]['Close']
        gdp_val = x_new_data_norm.iloc[-1]['GDP']
        inf_val = x_new_data_norm.iloc[-1]['InflationRate']

        x_new_data = [stock_val, gdp_val, inf_val, avg_sentiment]

        x_new_data = np.array(x_new_data)
        x_new_data = x_new_data.reshape(1, 1, len(x_new_data))

        prediction = np.argmax(model.predict(x_new_data), axis=1)

        return prediction, latest_close

    @classmethod
    def get_current_model():
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)

        return os.environ["MARKET_MODEL_VER"] 
    
    @classmethod
    def trend_accuracy(self, version):
        model = MarketModelUtils.load_model(version)
        x_train, y_train, x_val, y_val =  MarketModelDataUtils.collect_data("AAPL", "")
        y_train_categorical = to_categorical(y_train, num_classes=3)
        y_val_categorical = to_categorical(y_val, num_classes=3)
                        
        # Explainable AI
        # ---------------------------------------
        # Showcases here, by using the AAPL data as an example, how the model came to its decision, and which features influenced its prediction the most
        explainer = lime_tabular.RecurrentTabularExplainer(x_train, training_labels=y_train_categorical, feature_names=['Close', 'GDP', 'Inflation', 'sentiment'], class_names=['-1', '0', '1'], mode='classification')
        exp = explainer.explain_instance(x_val[0], model.predict, top_labels=True, num_features=240)
        
        # Saves as an HTML file that can be loaded, and that can be visited by the admin upon request
        exp.save_to_file('server/application/prediction/market_model/trend_explanation.html')
        diagnostics = model.evaluate(x_val, y_val_categorical)
        predicted_trends = np.argmax(MarketModelUtils.load_model(version).predict(x_val), axis=1)
            
        # Creating a Seaborn heatmap to show how good the model is at predicting the market trend
        mtrx = confusion_matrix(y_val, predicted_trends)
        sns.heatmap(mtrx, annot=True, fmt=".0f")
        img_path = 'heatmap-mkt.png'
        plt.savefig(img_path)
        plt.clf()

        with open(img_path, "rb") as image:
            heatmap = base64.b64encode(image.read()).decode('utf-8')

        return {"summary": MarketModelUtils.load_model(version).to_json(), "loss": diagnostics[0], "accuracy": diagnostics[1], "heatmap": heatmap}

    @classmethod
    def set_trend_model(self, version):
    # Update the environment variable for the current process
        os.environ["MARKET_MODEL_VER"] = version

        # Update the .env file
        env_file_path = '.env'
        with open(env_file_path, 'r') as file:
            lines = file.readlines()

        # Modify the lines list with the new value
        modified_lines = []
        for line in lines:
            if line.startswith(f'{"MARKET_MODEL_VER"}='):
                line = f'{"MARKET_MODEL_VER"}={version}\n'
            modified_lines.append(line)

        # Write the modified lines back to the file
        with open(env_file_path, 'w') as file:
            file.writelines(modified_lines)

        # Reload the updated .env file
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)

        return version
