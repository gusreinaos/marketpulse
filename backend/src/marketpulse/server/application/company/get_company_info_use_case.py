# Author: Michael Larsson

from ...infrastructure.repositories.company_repository import CompanyRepository
from ...application.serializers.company_serializer import CompanySerializer, CompanyListSerializer
import pandas as pd

class CompanyInfoUseCase:
    def getCompanyInfo(company:str):
        unserialized_companies = CompanyRepository.getByCode(company)

        serializer = CompanyListSerializer(unserialized_companies)
        response = serializer.data

        return response