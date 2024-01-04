import pandas as pd
from ..repositories.train_trend_data_repository import TrainTrendDataRepository

def get_tweet_sentiments(company, data_file): 
    #THE FOLLOWING TAKES ALL TWEETS AND SOME OF THEIR COLUMNS. CONVERTS IT TO DATAFRAME AND CHANGES DATE FORMAT.
    #Filtering the tweets to only contian certain columns
    tweet_col_names = ["tweet_id", "post_date", "body", "comment_num", "retweet_num", "like_num", "sentiment"]
    #Reading the tweet csv file
    tweet_df = pd.DataFrame
    if data_file=="":
        tweet_df = TrainTrendDataRepository.getByCmp(company)
        tweet_df = pd.DataFrame.from_records(tweet_df)
    else:
        tweet_data = pd.read_csv(data_file, usecols=tweet_col_names)
        #Converting the tweet data to a dictionary
        tweet_df = pd.DataFrame(tweet_data)
    
    #Converting the tweets post date from epoch into y-m-d format
    tweet_df['post_date'] = pd.to_datetime(tweet_df['post_date'], unit='s').dt.strftime('%Y-%m-%d')
    tweet_df.rename(columns={"post_date": "Date"}, inplace=True)

    specific_average_sentiment = tweet_df.groupby('Date')['sentiment'].mean().reset_index()

    specific_average_sentiment.set_index('Date', inplace=True)

    specific_average_sentiment.index = pd.to_datetime(specific_average_sentiment.index)

    return specific_average_sentiment