# Author: Burak Askan

import pandas as pd
from ..repositories.train_trend_data_repository import TrainTrendDataRepository

def get_tweet_sentiments(company, data_file): 
    #THE FOLLOWING TAKES ALL TWEETS AND SOME OF THEIR COLUMNS. CONVERTS IT TO DATAFRAME AND CHANGES DATE FORMAT.
    #Filtering the tweets to only contian certain columns
    tweet_col_names = ["post_date","sentiment", "ticker_symbol"]
    #Reading the tweet csv file
    tweet_df = pd.DataFrame
    if data_file=="":
        tweet_df = TrainTrendDataRepository.getByCmp(company)
        tweet_df = pd.DataFrame.from_records(tweet_df)
    else:
        try:
            tweet_data = pd.read_csv(data_file, usecols=tweet_col_names)
            #Converting the tweet data to a dictionary
            tweet_df = pd.DataFrame(tweet_data)
            missing_columns = [col for col in tweet_col_names if col not in tweet_df.columns]
            if missing_columns:
                raise Exception(f"The given csv files is missing column(s). Make sure all the following columns exist: {tweet_col_names}")
            for value in tweet_df['sentiment'].values.tolist():
                if int(value) != 0 and int(value) != 1 and int(value) != 2:
                    raise Exception("The given sentiments are incorrect and not labeled according to the following format: 0 for negative, 1 for neutral or 2 for positive.")
        except Exception as e:
            print(e)
            return e 
        

    #Converting the tweets post date from epoch into y-m-d format
    tweet_df['post_date'] = pd.to_datetime(tweet_df['post_date'], unit='s').dt.strftime('%Y-%m-%d')
    tweet_df.rename(columns={"post_date": "Date"}, inplace=True)

    specific_average_sentiment = tweet_df.groupby('Date')['sentiment'].mean().reset_index()

    specific_average_sentiment.set_index('Date', inplace=True)

    specific_average_sentiment.index = pd.to_datetime(specific_average_sentiment.index)

    first_date = specific_average_sentiment.index.min()
    last_date = specific_average_sentiment.index.max()
    return specific_average_sentiment, first_date, last_date