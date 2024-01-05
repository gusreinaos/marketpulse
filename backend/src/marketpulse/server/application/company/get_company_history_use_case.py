# Author: Michael Larsson

from ...infrastructure.repositories.yahoo_api_repository import YahooAPIRepository
import pandas as pd

class CompanyHistoryUseCase:
    def getCompanyHistory(company:str):
        response = YahooAPIRepository.getCompanyHistory(company)
        response.index = pd.to_datetime(response.index, unit='s').strftime('%Y-%m-%d')
        response = response.reset_index()
        response.rename(columns={'Date':'time', 'Close':'value'}, inplace=True)
        columns = ['time', 'value']
        response_data = response[columns].to_dict(orient='index')
        return response_data