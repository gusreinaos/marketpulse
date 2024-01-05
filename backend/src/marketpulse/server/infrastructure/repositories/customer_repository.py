# Author: John Berntsson

from ...models import CustomUser,UserFavoritesCompany

class CustomerRepository:
    @classmethod
    def save(cls, customer):
        """
        Save a customer to the database.

        Args:
            customer (Customer): The customer instance to be saved.

        Returns:
            Customer: The saved customer instance.
        """
        customer.save()
        return customer

    @classmethod
    def getById(cls,cid:str) -> CustomUser:
        """
        Gets a customer from the database.

        Args:
            cid (String): The customer id to be fetched.

        Returns:
            Customer: The customer instance.
        """
        customer = CustomUser.objects.get(id=cid)
        return customer

    @classmethod
    def getCompaniesByUser(cls,cid:str):
        companies = UserFavoritesCompany.objects.filter(user=cid)
        return companies

    @classmethod
    def addFavoriteToUser(cls,usrFavsCmp):
        usrFavsCmp.save()
        return usrFavsCmp
    
    @classmethod
    def removeFavoriteFromUser(cls,cid:str,cmp:str):
        entry = UserFavoritesCompany.objects.filter(user=cid,company=cmp).delete()
        return entry