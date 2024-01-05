# Author: Wojciech Pechmann, Michael Larsson

from ...models import Company

class CompanyRepository:
    @classmethod
    def save(cls, company):
        """
        Save a Company to the database.

        Args:
            Company (Company): The Company instance to be saved.

        Returns:
            Company: The saved Company instance.
        """
        company.save()
        return company

    def getById(cls,cmp:str) -> Company:
        """
        Gets a Company from the database.

        Args:
            cid (String): The Company id to be fetched.

        Returns:
            Company: The Company instance.
        """
        company = Company.objects.get(company_code=cmp)
        return company
    
    def get_all():
        companies = Company.objects.all()
        return companies
    
    def get_trainable_companies():
        companies = Company.objects.filter(trainable=1)
        return companies
    
    @classmethod
    def getByCode(self, c_code):
        try:
            return Company.objects.all()[:6]
        except Company.DoesNotExist:
            return None
