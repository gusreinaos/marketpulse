# Author: Michael Larsson

from ...infrastructure.repositories.yahoo_api_repository import YahooAPIRepository
import pandas as pd

class StockTrendUseCase:
    def getStockTrend(company:str):
        response = YahooAPIRepository.getStockTrend(company)
        response.index = pd.to_datetime(response.index, unit='s').strftime('%Y-%m-%d')
        response = response.reset_index()
        trend = response.at[0, 'Close'] - response.at[0, 'Open']
        return trend