// src/services/customerService.ts
import axios from 'axios';
import { Customer } from '../domain/entities/customer';

const API_BASE_URL = 'http://localhost:8000';

const AuthService = {
  signIn: async (username: string, password: string) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/auth/login`,{
          username: username,
          password: password,
        }
      );
      console.log(response.data)
      return response.data;

    } catch (error: any) {
      throw error.response.data;
    }
  },
};

export default AuthService;
