# Author: John Berntsson, Oscar Reina

from ...models import Customer
from ...infrastructure.repositories.customer_repository import CustomerRepository
import uuid

class GetCustomerUseCase:
    @classmethod
    def get_customer(customer_name):
        customer =  CustomerRepository.get_by_name(customer_name=customer_name)
        return customer

