import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

end_date = datetime.now().strftime('%Y-%m-%d')
cmp = yf.Ticker('AAPL')
cmp_history = cmp.history(start='2010-01-01', end=end_date)

class YahooAPIRepository:
    @classmethod
    def getCompanyHistory(self, code: str):
        try: 
            cmp = yf.Ticker(code)
            cmp_history = cmp.history(start='2010-01-01', end=end_date)
            return cmp_history
        except:
            print("An error with the company history occurred!")
    
    @classmethod
    def getStockTrend(self, code: str):
        try: 
            yesterday_date = (datetime.now()) - timedelta(days=1)
            cmp = yf.Ticker(code)
            cmp_trend = cmp.history(start='2023-11-20', end=end_date)
            return cmp_trend
        
        except:
            print("An error with the company history occurred!")
    
    
    """
    Gets the stock data of a company

    Args:
        start_date: YYYY-MM-DD format string date. Should be an earlier date than the latest_date. The earliest date of the data
        latest_date: YYYY-MM-DD format string date. Should be a later date than the latest_date. The latest date of the data.

    Returns:
        dataframe: A dataframe containing the close price with date as index

    Raises:
        serializers.ValidationError: If input data is not valid.
        IntegrityError: If there is an integrity violation during saving.
    """ 
    @classmethod
    def get_finance_date(self, start_date, latest_date, company):
        yf.pdr_override()
        stock_data = yf.download(company, start_date, latest_date)

        close_price = stock_data['Close']
        close_price_data = pd.DataFrame(close_price)
        close_price_data.rename(columns={"date": "Date"}, inplace=True) 
        close_price_data.drop(close_price_data.index[0])
        close_price_data_resampled = close_price_data.resample('D').mean().interpolate() 
        
        return close_price_data_resampled


    




