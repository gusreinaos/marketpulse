# Author: Wojciech Pechmann, Burak Askan

from ...models import CustomUser
from ...infrastructure.repositories.customer_repository import CustomerRepository
from ...infrastructure.repositories.prediction_repository import PredictionRepository
from ...infrastructure.repositories.company_repository import CompanyRepository
from ..serializers.company_serializer import CompanySerializer
from ..serializers.customer_favorites_company_serializer import CustomerFavoritesCompanySerializer

import pandas as pd

class GetFavoritesUseCase:  
    @classmethod 
    def get(self,customer_id):
        user_companies = CustomerRepository.getCompaniesByUser(customer_id)
        latest_predictions = PredictionRepository.get_latest()
        user_company_data = [{'company_code': user_companies.company.company_code, 'company_name': user_companies.company.company_name} for user_companies in user_companies]

        merged_df = pd.merge(pd.DataFrame.from_records(user_company_data), latest_predictions, how='inner', on='company_code')

        return merged_df.to_json(orient='records')