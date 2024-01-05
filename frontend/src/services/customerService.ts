//Author: Oscar Reina, John Berntsson
import axios from 'axios';
import { Customer } from '../domain/entities/customer';
import { CompanyPrediction } from '../domain/entities/companyPrediction';



const API_BASE_URL = 'http://34.122.134.118:8000'; 

const CustomerService = {
  createCustomer: async (customerData: Customer) => {
    try {
      console.log(customerData)
      const response = await axios.post(`${API_BASE_URL}/api/auth/signup`, customerData);
      console.log(response.data)
      return response.data; 
    } catch (error: any) {
      console.log(error)
      throw error.response.data; 
    }
  },
  
  updateCustomer: async (userId:string, customerData:any) => {
    try {
      const response = await axios.patch(`${API_BASE_URL}/api/customers/${userId}`, customerData);
      console.log(response.data)
      return response.data; 
    } catch (error: any) {
      throw error.response.data; 
    }
  },
  
  getCustomerById: async (customerId: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/customers/${customerId}`);
      return response.data; 
    } catch (error: any) {
      throw error.response.data; 
    }
  },

  deleteCustomer: async (customerId: string) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}/api/customers/${customerId}`);
      return response.data; 
    } catch (error: any) {
      throw error.response.data; 
    }
  },

  addCustomerFavoriteCompany: async (customerId: string, companyId: string) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/customers/${customerId}/favorites/${companyId}`)
      return response.data;
    } catch(error: any){
      throw error.response.data;
    }
  },
  removeCustomerFavoriteCompany: async (customerId: string, companyId: string) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}/api/customers/${customerId}/favorites/${companyId}/1`)
      return response.data;
      
    } catch(error: any){
      throw error.response.data;
    }
  },
  getCustomerFavorites: async (customerId: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/customers/${customerId}/favorites`)
      const list = eval(response.data) as CompanyPrediction[];
      



      console.log(list)
      return list;
    } catch(error: any){
      throw error.response.data;
    }
  },
  

};

export default CustomerService;
