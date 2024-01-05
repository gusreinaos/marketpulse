# Author: Burak Askan, Michael Larsson

import requests
import pandas as pd

api_key = 'ad44af7d85988ce68aab2abc0e32cf28'

"""
        Fetches requested type of economic data for a certain time period

        Args:
            series_id (String): Code for specific economic data.
            start_date: A string date with the format YYYY-MM-DD. The earliest data.
            end_date: A string date with the format YYYY-MM-DD. The latest data.

        Returns:
            DataFrame: A dataframe containing the data requested with the datetime as the index.

        Raises:
            serializers.ValidationError: If input data is not valid.
            IntegrityError: If there is an integrity violation during saving.
"""

def get_fred_data(series_id, start_date, end_date):
    try:
        base_url = 'https://api.stlouisfed.org/fred'
        endpoint = '/series/observations'

        # Construct the full URL
        url = f'{base_url}{endpoint}?series_id={series_id}&api_key={api_key}&observation_start={start_date}&observation_end={end_date}&file_type=json'

        # Make the API request
        response = requests.get(url)
        columns_needed = ['value']

        

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract and return the data
            data = response.json()

            data =  pd.DataFrame(data['observations'])
             # Make the API request
            missing_columns = [col for col in columns_needed if col not in data.columns]
            if missing_columns:
                raise Exception(f"The given data from FRED API is missing column(s). Make sure all the following columns exist: {columns_needed}, for the following code: {series_id}")
            for value in data['value'].values.tolist():
                if float(value)  <= 0 :
                    raise Exception(f"Given values from FRED contain values that are zero or below at the following code: {series_id}.")

            return data
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(e)
        return e



"""
        Performs required data manipulation when fetching the GDP data

        Args:
            start_date: A string date with the format YYYY-MM-DD. The earliest data.
            end_date: A string date with the format YYYY-MM-DD. The latest data.

        Returns:
            DataFrame: A dataframe containing the GDP with the datetime as the index.

        Raises:
            serializers.ValidationError: If input data is not valid.
            IntegrityError: If there is an integrity violation during saving.
"""
def getGDPData(start_date, latest_date):
    try:
        gdp_series_id = 'GDPC1'  # Real Gross Domestic Product, Chained Dollars
        gdp_data = get_fred_data(gdp_series_id, start_date, latest_date) #The expected for format is '2015-01-01'
        #Convert the date column into the datetime datatype
        gdp_data['date'] = pd.to_datetime(gdp_data['date']) 
        #Convert the value into numeric datatype
        gdp_data['value'] = pd.to_numeric(gdp_data['value'], errors='coerce', downcast='float')# coerce to NaN for non-numeric values
        #Set the key index to be the date
        gdp_data.set_index('date', inplace=True)
        #Set the index to be of type DatetimeIndex
        gdp_data.index = pd.to_datetime(gdp_data.index)
        #gdp_data = gdp_data.resample('D').mean().interpolate() TODO: THERE IS NOTHING TO INTERPOLERATE IF WE ARE ONLY TAKING LATEST AJUST FOR TRAINING
        return gdp_data['value']
    except Exception as e:
        print(e)
        return e

"""
        Performs required data manipulation when fetching the Inflation data

        Args:
            start_date: A string date with the format YYYY-MM-DD. The earliest data.
            end_date: A string date with the format YYYY-MM-DD. The latest data.

        Returns:
            DataFrame: A dataframe containing the Inflation with the datetime as the index.

        Raises:
            serializers.ValidationError: If input data is not valid.
            IntegrityError: If there is an integrity violation during saving.
"""

def getInflationData(start_date, latest_date): 
    try:
        inflation_series_id = 'CPIAUCNS'
        #Retrieving inflation data for US
        inflation_data = get_fred_data(inflation_series_id, start_date, latest_date)
        inflation_data['value'] = pd.to_numeric(inflation_data['value'], errors='coerce', downcast='float')
        #Setting the index to the date
        inflation_data.set_index('date', inplace=True)
        #Converting the index into a DatetimeIndex
        inflation_data.index = pd.to_datetime(inflation_data.index)
        #inflation_data = inflation_data.resample('D').mean().interpolate()TODO: THERE IS NOTHING TO INTERPOLERATE IF WE ARE ONLY TAKING LATEST AJUST FOR TRAINING
        return inflation_data['value']
    except Exception as e:
        print(e)
        return e
