# Author: Aditya Khadkikar, Wojciech Pechmann

import numpy as np
import pandas as pd
import tensorflow as tf
import os
import dotenv
from marketpulse.settings import BASE_DIR
from .tweet_cleaner_utils import TweetCleanerUtils
import pandas as pd, numpy as np
import sys, os, base64, seaborn as sns
import dotenv
from marketpulse.settings import BASE_DIR
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

from .tweet_cleaner_utils import TweetCleanerUtils
from .....infrastructure.repositories.train_sentiment_data_repository import TrainSentimentDataRepository
from .....infrastructure.repositories.valid_sentiment_data_repository import ValidSentimentDataRepository
from .....models import TrainSentimentData
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from keras.utils import to_categorical
from lime.lime_text import LimeTextExplainer

class SentimentModelUtils:
    @classmethod
    def analyze_tweets(self, tweets, model_ver : int): 
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)

        model_ver =  os.environ["SENTIMENT_MODEL_VER"]
        model = SentimentModelUtils.get_model(model_ver)
        
        tweet_arr =[]
        for tweet in tweets:
            c_tweet = TweetCleanerUtils.clean_tweet(tweet)
            tweet_arr.append(c_tweet)
            
        model_input = tf.constant(tweet_arr)

        result = SentimentModelUtils.run_model(model,model_input)

        return result

    @classmethod
    def run_model(self, model, input):
        #Method made since the model changes frequently so the way to run it benefits from being separate from the rest of the code.
        prediction = np.argmax(model.predict(input), axis=1)
        sentiment_list = np.copy(prediction)

        temp = -1
        sentiment_list[sentiment_list == 2] = temp
        sentiment_list[sentiment_list == 1] = 2
        sentiment_list[sentiment_list == temp] = 1
        print("Sentiments", sentiment_list)

        return prediction

    @classmethod
    def set_sentiment_model(self, version):
        # Update the environment variable for the current process
        os.environ["SENTIMENT_MODEL_VER"] = version

        # Update the .env file
        env_file_path = '.env'
        with open(env_file_path, 'r') as file:
            lines = file.readlines()

        # Modify the lines list with the new value
        modified_lines = []
        for line in lines:
            if line.startswith(f'{"SENTIMENT_MODEL_VER"}='):
                line = f'{"SENTIMENT_MODEL_VER"}={version}\n'
            modified_lines.append(line)

        # Write the modified lines back to the file
        with open(env_file_path, 'w') as file:
            file.writelines(modified_lines)

        # Reload the updated .env file
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        
        # Print the updated environment variable value
        print(os.environ["SENTIMENT_MODEL_VER"])

        return version

    @classmethod
    def get_model(self, version: str):
        path = os.path.join(BASE_DIR, f'server/application/prediction/sentiment_model/versions/{version}/model')
        model = tf.keras.models.load_model(os.path.abspath(os.path.expanduser(path)))
        return model
    
    @classmethod
    def get_accuracy(self, version: str):
        # Access the dataset that was set aside just for accuracy testing of the model versions.        
        # Convert to DataFrame
        test_df = pd.DataFrame(list(ValidSentimentDataRepository.getCleanRows()), columns=['text', 'label'])
        test_df['label'] = test_df['label'].replace({-1:0})
        
        try:
            # Should return an array where [index0: loss, index1: accuracy]
            model = SentimentModelUtils.get_model(version)
            diagnostics = model.evaluate(test_df['text'], test_df['label'])  

        except ValueError:
            # Make the y-values into one-hot encoded arrays, as the loss function requires it in the format
            y_hot = tf.keras.utils.to_categorical(test_df['label'])
            diagnostics = SentimentModelUtils.get_model(version).evaluate(test_df['text'], y_hot)  
        
        # Explainable AI
        # ---------------------------------------
        # By using sample data (the 152nd data point), as an example, showcases how the model came to its decision, 
        # and which features influenced its prediction the most.
        sample_idx = 150
        predicted_sentiments = np.argmax(model.predict([test_df['text'][sample_idx]]), axis=1)
        print(predicted_sentiments)
        print(np.argmax(y_hot, axis=1))

        class_names = ['0', '1', '2']
        explainer = LimeTextExplainer(class_names=class_names)
        exp = explainer.explain_instance(test_df['text'][sample_idx], model.predict, top_labels=True)
        exp.save_to_file("server/application/prediction/sentiment_model/sentiment_explanation.html")

        predicted_sentiments = np.argmax(SentimentModelUtils.get_model(version).predict(test_df['text']), axis=1)
        print("Sentiments", predicted_sentiments)
        
        # Creating a Seaborn heatmap to show how good the model is at predicting the tweet's sentiments
        mtrx = confusion_matrix(test_df['label'], predicted_sentiments)
        sns.heatmap(mtrx, annot=True, fmt=".0f")
        img_path = 'heatmap.png'
        plt.savefig(img_path)
        plt.clf()

        with open(img_path, "rb") as image:
            heatmap = base64.b64encode(image.read()).decode('utf-8')

        return {
            "summary": SentimentModelUtils.get_model(version).to_json(), 
            "loss": diagnostics[0], 
            "accuracy": diagnostics[1],
            "heatmap": heatmap
        }
    
    @classmethod
    def get_production_model(self):
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)

        model_ver =  os.environ["SENTIMENT_MODEL_VER"]
        return model_ver