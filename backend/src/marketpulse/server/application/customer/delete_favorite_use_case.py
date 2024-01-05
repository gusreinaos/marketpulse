# Author: Wojciech Pechmann

from ...models import CustomUser
from ...infrastructure.repositories.customer_repository import CustomerRepository
from ...infrastructure.repositories.company_repository import CompanyRepository
from ..serializers.customer_favorites_company_serializer import CustomerFavoritesCompanySerializer

class DeleteFavoriteUseCase:
    @classmethod
    def delete(self,customer_id,company_id):
        company = CustomerRepository.removeFavoriteFromUser(customer_id,company_id)
        return {"message":'ok','data':{'customer_id':customer_id,'company_id':company_id}}