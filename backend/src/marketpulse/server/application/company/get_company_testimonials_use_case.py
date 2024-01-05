# Author: Michael Larsson

from ...infrastructure.repositories.stocktwit_api_repository import StocktwitApiRepository
from datetime import datetime

class CompanyTestimonialUseCase:
    def convertApostrophe(inputText):
        if '&#39;' in inputText:
            convertedText = inputText.replace('&#39;', "'")
            return convertedText
        else:
            return inputText
        
    def convertQuote(inputText):
        if '&quot;' in inputText:
            convertedText = inputText.replace('&quot;', '"')
            return convertedText
        else:
            return inputText
        
    def formatDateTime(inputTime):
        datePart, timePart = inputTime.split('T')
        timePart = timePart[:-1]

        hourPart, minutePart, _ = timePart.split(':')
        formattedTime = f"{datePart}, {hourPart}:{minutePart}"
        return formattedTime
        
    def getTestimonials(company: str):
        response = StocktwitApiRepository.get_stocktwits_for_company(company)

        for message in response:
            message['body'] = CompanyTestimonialUseCase.convertApostrophe(message['body'])
            message['body'] = CompanyTestimonialUseCase.convertQuote(message['body'])
            message['created_at'] = CompanyTestimonialUseCase.formatDateTime(message['created_at'])

        return response
    

    