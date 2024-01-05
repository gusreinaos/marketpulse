# Author: Wojciech Pechmann, Burak Askan

from ...models import Company
from ...infrastructure.repositories.company_repository import CompanyRepository
from ...infrastructure.repositories.prediction_repository import PredictionRepository

import pandas as pd

class GetAllPredictions:  
    @classmethod 
    def get(self):
        latest_predictions = PredictionRepository.get_latest()
        all_companies = CompanyRepository.get_all()        
        all_companies = [{'company_code': company.company_code, 'company_name': company.company_name} for company in all_companies]

        merged_df = pd.merge(pd.DataFrame.from_records(all_companies), pd.DataFrame.from_records(latest_predictions), how='inner', on='company_code')
        print(merged_df)

        return merged_df.to_json(orient='records')