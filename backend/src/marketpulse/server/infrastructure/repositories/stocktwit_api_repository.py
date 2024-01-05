# Author: John Berntsson, Wojciech Pechmann

import requests
import json
import time

class StocktwitApiRepository:

    """
    Retrieves StockTwits data for a specific company.

    Args:
        company_name (str): The symbol or identifier of the company.

    Returns:
        bytes: The raw content of the response from the StockTwits API.

    Raises:
        Exception: Any exception that occurs during the request.
    """

    def get_stocktwits_for_company(company_name: str):
        try:
            # Set up cookies for the request
            cookies = {
                'auto_log_in': '1',
                'enw': '1',
                'anonymous_user_id': 'anonymous-OTHERS-WEB-1',
            }

            # Set up headers for the request
            headers = {
                'authority': 'api.stocktwits.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9,sv;q=0.8',
                'cache-control': 'max-age=0',
                # 'cookie': 'auto_log_in=1; enw=1; anonymous_user_id=anonymous-OTHERS-WEB-1',
                'if-none-match': 'W/"ac7454bff331f47082d7f0f4f27c4a39"',
                'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            }

            # Make a GET request to StockTwits API
            response = requests.get('https://api.stocktwits.com/api/2/streams/symbol/' + company_name + '.json', cookies=cookies, headers=headers)
            # Uncomment the line below for debugging purposes
            # print(response.content)

            byte_content= response.content

            resp_dict = json.loads(byte_content.decode('utf-8'))

            return resp_dict.get('messages')

        except Exception as e:
            # Handle and print any exceptions that occur
            print(f"Error: {e}")

