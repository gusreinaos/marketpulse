//Author: Oscar Reina, John Berntsson
import axios from 'axios';

export interface Admin {
    adminId: string;
    adminName: string;
    adminEmail: string;
    adminPassword: string;
}

const API_BASE_URL = 'http://34.122.134.118:8000'; 

export const customerService = {
    createAdmin: async (adminCreds: Admin) => {
        try {
          console.log(adminCreds)
          const response = await axios.post(`${API_BASE_URL}/api/admins`, adminCreds);
          return response.data; 
        } catch (error: any) {
          throw error.response.data; 
        }
    }
}