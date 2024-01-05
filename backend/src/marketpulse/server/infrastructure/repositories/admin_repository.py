# Author: John Berntsson

class AdminRepository:
    @classmethod
    def save(cls, admin):
        """
        Save a customer to the database.

        Args:
            customer (Customer): The customer instance to be saved.

        Returns:
            Customer: The saved customer instance.
        """
        admin.save()
        return admin

 
