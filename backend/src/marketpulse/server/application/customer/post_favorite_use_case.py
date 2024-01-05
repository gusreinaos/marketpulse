# Author: Wojciech Pechmann

from ...models import CustomUser,UserFavoritesCompany
from ...infrastructure.repositories.customer_repository import CustomerRepository
from ...infrastructure.repositories.company_repository import CompanyRepository
from ..serializers.customer_favorites_company_serializer import CustomerFavoritesCompanySerializer

class PostFavoriteUseCase:
    @classmethod
    def post(self,customer_id,company_id):

        serializer = CustomerFavoritesCompanySerializer(data={
            'user':customer_id,
            'company':company_id
        })

        serializer.is_valid(raise_exception=True)

        new_entry = UserFavoritesCompany(
            user=serializer.validated_data['user'],
            company=serializer.validated_data['company']
        )

        company = CustomerRepository.addFavoriteToUser(new_entry)
        
        return serializer.data