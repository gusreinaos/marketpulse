# Author: Aditya Khadkikar

import tensorflow as tf
import pandas as pd, numpy as np
import sys, os, csv, base64, seaborn as sns
import dotenv
import traceback, glob
import logging, datetime
from marketpulse.settings import BASE_DIR
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
from sklearn.model_selection import train_test_split
from rest_framework import serializers
from .utils.tweet_cleaner_utils import TweetCleanerUtils
from .utils.sentiment_model_utils import SentimentModelUtils
from ....infrastructure.repositories.train_sentiment_data_repository import TrainSentimentDataRepository
from ....infrastructure.repositories.valid_sentiment_data_repository import ValidSentimentDataRepository
from ....models import TrainSentimentData
from ....models import ValidSentimentData
from ...serializers.train_sentiment_data_serializer import TrainSentimentDataSerializer
from ...serializers.valid_sentiment_data_serializer import ValidSentimentDataSerializer
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

class TrainSentimentModelUseCase:
    @classmethod
    def train(self, version: str, training_file: str, EPOCHS=10, BATCH_SIZE=32):
        try:
            # Getting the file from the frontend
            raw_csv = StringIO(training_file)
            
            # Should be given as the name in every new created version of model
            today_date = datetime.datetime.now()
            print(today_date)
            
            # Reading the string, and adding it to a file, to make it readable for the tweet_cleaner preprocessing script
            df = pd.read_csv(raw_csv).replace({-1:0})
            df.to_csv(os.path.join(BASE_DIR, 'server/application/prediction/sentiment_model/new_unclean.csv'))
            
            # Cleaning + convert to df, in order to be sent for training to the particular model version chosen
            TweetCleanerUtils.clean_labeled_CSV('new_unclean.csv', 'new_clean.csv', 'text', 'label')
            df_clean = pd.read_csv('new_clean.csv').replace({-1:0})
            
            # A part of the newly submitted data by the admin will go to the train_db, and val_db respectively.
            df_unclean_train = df[['text', 'label']].iloc[:int(0.7*len(df_clean))]
            df_unclean_val = df[['text', 'label']].iloc[int(0.7*len(df_clean)):]
            df_clean_train = df_clean[['text', 'label']].iloc[:int(0.7*len(df_clean))]
            df_clean_val = df_clean[['text', 'label']].iloc[int(0.7*len(df_clean)):]
            
            # Convert each row of df to be serialized, to be added to the training db
            for i in range(len(df)):
                serializer = TrainSentimentDataSerializer(data={
                    'vs_id': '',
                    'unclean': df['text'].iloc[i],
                    'clean': df_clean['text'].iloc[i],
                    'sentiment': df_clean['label'].iloc[i],
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

                saved_data = TrainSentimentDataRepository.save(new_data)
            
            for i in range(len(df_unclean_val)):
                val_serializer = ValidSentimentDataSerializer(data={
                    'vs_id': '',
                    'unclean': df_unclean_val['text'].iloc[i],
                    'clean': df_clean_val['text'].iloc[i],
                    'sentiment': df_clean_val['label'].iloc[i],
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
            
            # Get the version of the model to train on top of.
            model = SentimentModelUtils.get_model(version)

            # Train model, with passing data from the train + validation database as the val_data.
            train_df = pd.DataFrame(list(TrainSentimentDataRepository.getCurrentRows()), columns=['text', 'label'])
            val_df = pd.DataFrame(list(ValidSentimentDataRepository.getCurrentRows()), columns=['text', 'label'])
            
            # Converting the y-values to one-hot encoded arrays for fitting to the models
            y_hot = tf.keras.utils.to_categorical(train_df['label'], num_classes=3)
            y_val_hot = tf.keras.utils.to_categorical(val_df['label'], num_classes=3)

            # Calling the fit function
            try:
                model.fit(train_df['text'], y_hot, epochs=EPOCHS, shuffle=True, validation_data=(val_df['text'], y_val_hot), callbacks=[tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=2, mode='min')])
            except ValueError:
                model.fit(train_df['text'], train_df['label'], epochs=EPOCHS, shuffle=True, validation_data=(val_df['text'], val_df['label']), callbacks=[tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=2, mode='min')])         
            
            # Save a version by incrementing above, from retrieving the highest value of the most recent version saved until now.
            ver_names = glob.glob('server/application/prediction/sentiment_model/versions/**')
            versions = [os.path.basename(file) for file in ver_names]

            version_num = int(max(versions)[:2])+1
            if version_num < 10:
                version_name = f'0{version_num}-{today_date.strftime("%Y-%m-%d")}'
            else:
                version_name = f'{version_num}-{today_date.strftime("%Y-%m-%d")}'

            # Save the fitted model as a new model version
            model.save(f'server/application/prediction/sentiment_model/versions/{version_name}/model', save_format='tf')
            return version_name

        except KeyError:
            print("The provided CSV file does not match the schema required. Submit a CSV with two columns: 'text' and 'label'.")        
            return False
            
        except Exception as e:
            logging.error(traceback.format_exc())
            return False        