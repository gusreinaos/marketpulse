# Author: Michael Larsson

from ...infrastructure.repositories.fred_api_repository import *
import pandas as pd

class InflationTrendUseCase:
    def getInflationTrend():
        response = getInflationData('2023-09-01', '2023-11-30')
        response.index = pd.to_datetime(response.index, unit='s').strftime('%Y-%m-%d')
        response = response.reset_index()
        last_month = float(response.at[0, 'value'])
        this_month = float(response.at[1, 'value'])
        trend = this_month - last_month
        return trend