# Author: Micahel Larsson, Burak Askan

import pandas as pd
from .....models import TrainTrendData
from .....infrastructure.repositories.train_trend_data_repository import TrainTrendDataRepository

def save_data():
    # Replace 'your_csv_file.csv' with the path to your CSV file
    labels_path = '/home/burak/dit826/market-pulse/backend/src/marketpulse/server/application/prediction/market_model/trend_data/Tweet_new_labeled.csv'

    cmp_path='/home/burak/dit826/market-pulse/backend/src/marketpulse/server/application/prediction/market_model/trend_data/Company_Tweet.csv'

    tweet_col_names = ["tweet_id", "post_date", "body", "comment_num", "retweet_num", "like_num", "sentiment"]

    # Read CSV data into a pandas DataFrame
    labeled_data = pd.read_csv(labels_path,  usecols=tweet_col_names)

    cmp_data = pd.read_csv(cmp_path)

    labeled_data = pd.DataFrame(labeled_data)

    tweet_df = pd.merge(labeled_data, cmp_data, on='tweet_id')

    cols_to_keep = ['post_date', 'sentiment', 'ticker_symbol']

    tweet_df = tweet_df[cols_to_keep]


    print(tweet_df)
    
    # Convert DataFrame to a list of YourModel instances
    model_instances = [TrainTrendData(**row) for index, row in tweet_df.iterrows()]


    TrainTrendDataRepository.bulkCreate(model_instances)

